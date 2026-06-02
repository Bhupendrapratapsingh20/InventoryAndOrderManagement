from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check() -> dict:
    """Basic health check endpoint."""
    return {"status": "healthy"}


@router.get("/db")
async def health_check_db(db: AsyncSession = Depends(get_db)) -> dict:
    """Database connectivity health check."""
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar_one()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "detail": str(e)}
