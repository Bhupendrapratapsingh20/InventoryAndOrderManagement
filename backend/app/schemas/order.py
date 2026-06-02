import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID = Field(..., description="Product UUID")
    quantity: int = Field(..., gt=0, description="Quantity to order (must be > 0)")


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_order_item(cls, item: object) -> "OrderItemResponse":
        """Build response from an OrderItem ORM object with loaded product."""
        return cls(
            id=item.id,  # type: ignore[arg-type]
            product_id=item.product_id,  # type: ignore[arg-type]
            product_name=item.product.name if item.product else "Unknown",  # type: ignore[union-attr]
            quantity=item.quantity,  # type: ignore[arg-type]
            unit_price=item.unit_price,  # type: ignore[arg-type]
            subtotal=item.subtotal,  # type: ignore[arg-type]
        )


class OrderCreate(BaseModel):
    customer_id: uuid.UUID = Field(..., description="Customer UUID")
    shipping_address: Optional[str] = Field(
        None, max_length=500, description="Shipping address"
    )
    items: list[OrderItemCreate] = Field(
        ..., min_length=1, description="List of items to order"
    )


class OrderResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    customer_name: str
    status: str
    total_amount: float
    shipping_address: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_order(cls, order: object) -> "OrderResponse":
        """Build response from an Order ORM object with loaded relationships."""
        return cls(
            id=order.id,  # type: ignore[arg-type]
            customer_id=order.customer_id,  # type: ignore[arg-type]
            customer_name=f"{order.customer.first_name} {order.customer.last_name}" if order.customer else "Unknown",  # type: ignore[union-attr]
            status=order.status.value if hasattr(order.status, "value") else str(order.status),  # type: ignore[union-attr]
            total_amount=order.total_amount,  # type: ignore[arg-type]
            shipping_address=order.shipping_address,  # type: ignore[arg-type]
            created_at=order.created_at,  # type: ignore[arg-type]
            updated_at=order.updated_at,  # type: ignore[arg-type]
            items=[
                OrderItemResponse.from_order_item(item)
                for item in order.items  # type: ignore[union-attr]
            ],
        )


class OrderListResponse(BaseModel):
    total: int
    orders: list[OrderResponse]


class DashboardStats(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: list
    low_stock_count: int
    revenue: float
    recent_orders: list
