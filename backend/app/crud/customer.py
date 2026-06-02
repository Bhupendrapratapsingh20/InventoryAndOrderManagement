import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


async def get_customers(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[Customer], int]:
    """Get paginated list of customers and total count."""
    count_query = select(func.count()).select_from(Customer)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = (
        select(Customer).offset(skip).limit(limit).order_by(Customer.created_at.desc())
    )
    result = await db.execute(query)
    customers = list(result.scalars().all())

    return customers, total


async def get_customer(db: AsyncSession, customer_id: uuid.UUID) -> Customer | None:
    """Get a single customer by ID."""
    query = select(Customer).where(Customer.id == customer_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_customer_by_email(db: AsyncSession, email: str) -> Customer | None:
    """Get a single customer by email."""
    query = select(Customer).where(Customer.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_customer(
    db: AsyncSession, customer_data: CustomerCreate
) -> Customer:
    """Create a new customer."""
    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


async def update_customer(
    db: AsyncSession, customer_id: uuid.UUID, customer_data: CustomerUpdate
) -> Customer | None:
    """Update an existing customer. Returns None if not found."""
    customer = await get_customer(db, customer_id)
    if customer is None:
        return None

    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return customer


async def delete_customer(db: AsyncSession, customer_id: uuid.UUID) -> bool:
    """Delete a customer by ID. Returns True if deleted, False if not found."""
    customer = await get_customer(db, customer_id)
    if customer is None:
        return False

    await db.delete(customer)
    await db.commit()
    return True


async def get_customer_count(db: AsyncSession) -> int:
    """Get total number of customers."""
    query = select(func.count()).select_from(Customer)
    result = await db.execute(query)
    return result.scalar_one()
