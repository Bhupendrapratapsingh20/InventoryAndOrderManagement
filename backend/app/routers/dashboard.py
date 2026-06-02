from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order as order_crud
from app.database import get_db
from app.schemas.order import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
) -> DashboardStats:
    """Get dashboard statistics including totals and revenue."""
    stats = await order_crud.get_dashboard_stats(db)
    return DashboardStats(**stats)
