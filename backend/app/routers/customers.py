import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import customer as customer_crud
from app.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=CustomerListResponse)
async def list_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
) -> CustomerListResponse:
    """Get a paginated list of all customers."""
    customers, total = await customer_crud.get_customers(db, skip=skip, limit=limit)
    return CustomerListResponse(
        total=total,
        customers=[CustomerResponse.model_validate(c) for c in customers],
    )


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """Create a new customer. Email must be unique."""
    existing = await customer_crud.get_customer_by_email(db, customer_data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Customer with email '{customer_data.email}' already exists.",
        )
    customer = await customer_crud.create_customer(db, customer_data)
    return CustomerResponse.model_validate(customer)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """Get a customer by ID."""
    customer = await customer_crud.get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id '{customer_id}' not found.",
        )
    return CustomerResponse.model_validate(customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: uuid.UUID,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """Update a customer by ID."""
    customer = await customer_crud.update_customer(db, customer_id, customer_data)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id '{customer_id}' not found.",
        )
    return CustomerResponse.model_validate(customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a customer by ID."""
    deleted = await customer_crud.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id '{customer_id}' not found.",
        )
