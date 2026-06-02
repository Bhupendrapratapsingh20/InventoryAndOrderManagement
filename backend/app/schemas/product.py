import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be > 0)")
    quantity_in_stock: int = Field(0, ge=0, description="Quantity in stock")
    category: Optional[str] = Field(None, max_length=100, description="Product category")


class ProductCreate(ProductBase):
    sku: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z0-9\-]+$",
        description="Stock Keeping Unit (alphanumeric and hyphens only)",
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)


class ProductResponse(ProductBase):
    id: uuid.UUID
    sku: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    total: int
    products: list[ProductResponse]
