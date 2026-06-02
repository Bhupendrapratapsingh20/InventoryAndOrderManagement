import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def get_products(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[Product], int]:
    """Get paginated list of products and total count."""
    # Total count
    count_query = select(func.count()).select_from(Product)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Paginated list
    query = select(Product).offset(skip).limit(limit).order_by(Product.created_at.desc())
    result = await db.execute(query)
    products = list(result.scalars().all())

    return products, total


async def get_product(db: AsyncSession, product_id: uuid.UUID) -> Product | None:
    """Get a single product by ID."""
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_product_by_sku(db: AsyncSession, sku: str) -> Product | None:
    """Get a single product by SKU."""
    query = select(Product).where(Product.sku == sku)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
    """Create a new product."""
    product = Product(**product_data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(
    db: AsyncSession, product_id: uuid.UUID, product_data: ProductUpdate
) -> Product | None:
    """Update an existing product. Returns None if not found."""
    product = await get_product(db, product_id)
    if product is None:
        return None

    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: uuid.UUID) -> bool:
    """Delete a product by ID. Returns True if deleted, False if not found."""
    product = await get_product(db, product_id)
    if product is None:
        return False

    await db.delete(product)
    await db.commit()
    return True


async def get_low_stock_products(
    db: AsyncSession, threshold: int = 10
) -> list[Product]:
    """Get products with stock at or below the threshold."""
    query = (
        select(Product)
        .where(Product.quantity_in_stock <= threshold)
        .order_by(Product.quantity_in_stock.asc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_product_count(db: AsyncSession) -> int:
    """Get total number of products."""
    query = select(func.count()).select_from(Product)
    result = await db.execute(query)
    return result.scalar_one()
