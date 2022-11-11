from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.products import ProductDBDao, ProductNotFoundException, ProductExistsException
from schemas.products import ProductSchema
from dependencies import get_db

router = APIRouter(prefix="/products", tags=["products"])


class ProductOut(ProductSchema):
    pass


class ProductIn(ProductSchema):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None


@router.get("/", response_model=List[ProductOut])
async def list_products(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    products = ProductDBDao.list(db, limit=limit, offset=offset)
    return products


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    try:
        product = ProductDBDao.get(db, product_id)
        return product
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/", response_model=ProductOut)
async def create_product(product: ProductIn, db: Session = Depends(get_db)):
    try:
        new_product = ProductDBDao.insert(db, product)
        return new_product
    except ProductExistsException:
        raise HTTPException(
            status_code=400, detail=f"Product id({product.id}) already exists")


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        updated_product = ProductDBDao.update(db, product_id, product)
        return updated_product
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    try:
        ProductDBDao.delete(db, product_id)
        return {"message": f"Product ({product_id}) deleted"}
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")
