import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import product as product_crud
from app.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/low-stock", response_model=list[ProductResponse])
async def list_low_stock_products(
    threshold: int = Query(10, ge=0, description="Stock threshold"),
    db: AsyncSession = Depends(get_db),
) -> list[ProductResponse]:
    """Get products with stock at or below the given threshold."""
    products = await product_crud.get_low_stock_products(db, threshold=threshold)
    return [ProductResponse.model_validate(p) for p in products]


@router.get("", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
) -> ProductListResponse:
    """Get a paginated list of all products."""
    products, total = await product_crud.get_products(db, skip=skip, limit=limit)
    return ProductListResponse(
        total=total,
        products=[ProductResponse.model_validate(p) for p in products],
    )


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Create a new product. SKU must be unique."""
    existing = await product_crud.get_product_by_sku(db, product_data.sku)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with SKU '{product_data.sku}' already exists.",
        )
    product = await product_crud.create_product(db, product_data)
    return ProductResponse.model_validate(product)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Get a product by ID."""
    product = await product_crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{product_id}' not found.",
        )
    return ProductResponse.model_validate(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Update a product by ID."""
    product = await product_crud.update_product(db, product_id, product_data)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{product_id}' not found.",
        )
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a product by ID."""
    deleted = await product_crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{product_id}' not found.",
        )
