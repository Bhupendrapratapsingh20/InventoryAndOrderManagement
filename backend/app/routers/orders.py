import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order as order_crud
from app.database import get_db
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=OrderListResponse)
async def list_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
) -> OrderListResponse:
    """Get a paginated list of all orders with items."""
    orders, total = await order_crud.get_orders(db, skip=skip, limit=limit)
    return OrderListResponse(
        total=total,
        orders=[OrderResponse.from_order(o) for o in orders],
    )


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    """
    Create a new order.
    - Validates customer exists
    - Validates product stock availability
    - Decrements stock for each item
    - Calculates total amount
    """
    order = await order_crud.create_order(db, order_data)
    return OrderResponse.from_order(order)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    """Get an order by ID with all items and product details."""
    order = await order_crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id '{order_id}' not found.",
        )
    return OrderResponse.from_order(order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete an order and restore stock for all items."""
    deleted = await order_crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id '{order_id}' not found.",
        )
