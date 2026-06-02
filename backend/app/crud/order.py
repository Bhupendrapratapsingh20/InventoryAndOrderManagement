import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


async def get_orders(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[Order], int]:
    """Get paginated list of orders with eagerly loaded relationships."""
    # Total count
    count_query = select(func.count()).select_from(Order)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Paginated list with eager loading
    query = (
        select(Order)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
        )
        .offset(skip)
        .limit(limit)
        .order_by(Order.created_at.desc())
    )
    result = await db.execute(query)
    orders = list(result.scalars().unique().all())

    return orders, total


async def get_order(db: AsyncSession, order_id: uuid.UUID) -> Order | None:
    """Get a single order by ID with eagerly loaded relationships."""
    query = (
        select(Order)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
        )
        .where(Order.id == order_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, order_data: OrderCreate) -> Order:
    """
    Create a new order with full business logic:
    1. Verify customer exists
    2. Verify each product exists and has sufficient stock
    3. Create order and order items
    4. Calculate total amount
    5. Decrement stock for each product
    6. Commit atomically
    """
    # Step 1: Verify customer exists
    customer_query = select(Customer).where(Customer.id == order_data.customer_id)
    customer_result = await db.execute(customer_query)
    customer = customer_result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id '{order_data.customer_id}' not found.",
        )

    # Step 2: Verify products and check stock
    insufficient_stock: list[dict] = []
    products_map: dict[uuid.UUID, Product] = {}

    for item in order_data.items:
        product_query = select(Product).where(Product.id == item.product_id)
        product_result = await db.execute(product_query)
        product = product_result.scalar_one_or_none()

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id '{item.product_id}' not found.",
            )

        if product.quantity_in_stock < item.quantity:
            insufficient_stock.append(
                {
                    "product_id": str(product.id),
                    "product_name": product.name,
                    "requested": item.quantity,
                    "available": product.quantity_in_stock,
                }
            )

        products_map[item.product_id] = product

    # Step 3: Raise if any product has insufficient stock
    if insufficient_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Insufficient stock for one or more products.",
                "insufficient_items": insufficient_stock,
            },
        )

    # Step 4: Create the Order record
    order = Order(
        customer_id=order_data.customer_id,
        shipping_address=order_data.shipping_address,
        total_amount=0.0,
    )
    db.add(order)
    await db.flush()  # Get order.id without committing

    # Step 5: Create OrderItem records and calculate total
    total_amount: float = 0.0
    for item in order_data.items:
        product = products_map[item.product_id]
        unit_price = product.price
        subtotal = round(item.quantity * unit_price, 2)
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        db.add(order_item)

        # Step 6: Decrement stock
        product.quantity_in_stock -= item.quantity

    # Step 7: Set total amount
    order.total_amount = round(total_amount, 2)

    # Step 8: Commit atomically
    await db.commit()

    # Step 9: Refresh and return with relationships loaded
    refreshed_order = await get_order(db, order.id)
    if refreshed_order is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created order.",
        )
    return refreshed_order


async def delete_order(db: AsyncSession, order_id: uuid.UUID) -> bool:
    """
    Delete an order and restore stock for each item.
    Returns True if deleted, False if not found.
    """
    # Load order with items and products
    query = (
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
        )
        .where(Order.id == order_id)
    )
    result = await db.execute(query)
    order = result.scalar_one_or_none()

    if order is None:
        return False

    # Restore stock for each item
    for item in order.items:
        if item.product is not None:
            item.product.quantity_in_stock += item.quantity

    # Delete order (cascade deletes order items)
    await db.delete(order)
    await db.commit()
    return True


async def get_order_count(db: AsyncSession) -> int:
    """Get total number of orders."""
    query = select(func.count()).select_from(Order)
    result = await db.execute(query)
    return result.scalar_one()


async def get_dashboard_stats(db: AsyncSession) -> dict:
    """Get dashboard statistics."""
    # Total products
    product_count_q = select(func.count()).select_from(Product)
    product_count_result = await db.execute(product_count_q)
    total_products = product_count_result.scalar_one()

    # Total customers
    customer_count_q = select(func.count()).select_from(Customer)
    customer_count_result = await db.execute(customer_count_q)
    total_customers = customer_count_result.scalar_one()

    # Total orders
    order_count_q = select(func.count()).select_from(Order)
    order_count_result = await db.execute(order_count_q)
    total_orders = order_count_result.scalar_one()

    # Low stock products (threshold = 10) - return full product objects
    low_stock_q = (
        select(Product)
        .where(Product.quantity_in_stock <= 10)
        .order_by(Product.quantity_in_stock.asc())
        .limit(10)
    )
    low_stock_result = await db.execute(low_stock_q)
    low_stock_items = low_stock_result.scalars().all()
    low_stock_products = [
        {
            "id": str(p.id),
            "name": p.name,
            "sku": p.sku,
            "quantity_in_stock": p.quantity_in_stock,
        }
        for p in low_stock_items
    ]

    # Total revenue (sum of all order total amounts)
    revenue_q = select(func.coalesce(func.sum(Order.total_amount), 0.0))
    revenue_result = await db.execute(revenue_q)
    total_revenue = float(revenue_result.scalar_one())

    # Recent orders (last 5)
    recent_orders_q = (
        select(Order)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items),
        )
        .order_by(Order.created_at.desc())
        .limit(5)
    )
    recent_orders_result = await db.execute(recent_orders_q)
    recent_order_items = recent_orders_result.scalars().unique().all()
    recent_orders = [
        {
            "id": str(o.id),
            "customer_name": f"{o.customer.first_name} {o.customer.last_name}" if o.customer else "Unknown",
            "total_amount": o.total_amount,
            "items_count": len(o.items),
            "status": o.status.value if hasattr(o.status, "value") else str(o.status),
            "created_at": o.created_at.isoformat(),
        }
        for o in recent_order_items
    ]

    return {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "low_stock_products": low_stock_products,
        "low_stock_count": len(low_stock_products),
        "revenue": round(total_revenue, 2),
        "recent_orders": recent_orders,
    }
