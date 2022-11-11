
from typing import Optional, List
import sqlalchemy as sa
from sqlalchemy.orm import Session

from db import Base
from schemas.products import ProductSchema


class Product(Base):
    __tablename__ = "products"

    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String)
    price = sa.Column(sa.Integer)

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())


class ProductNotFoundException(Exception):
    pass


class ProductExistsException(Exception):
    pass


class ProductDBDao:
    @classmethod
    def get(cls, db: Session, product_id: str) -> Optional[ProductSchema]:
        db_product = db.query(Product).filter(
            Product.id == product_id).first()
        if db_product is None:
            raise ProductNotFoundException()
        return ProductSchema.from_orm(db_product)

    @classmethod
    def list(cls, db: Session, limit: int, offset: int) -> List[ProductSchema]:
        db_orm_products = db.query(Product).limit(limit).offset(offset).all()
        db_products = []
        for db_product in db_orm_products:
            db_products.append(ProductSchema.from_orm(db_product))
        return db_products

    @classmethod
    def insert(cls, db: Session, product: ProductSchema) -> None:
        indb = db.query(Product).filter(
            Product.id == product.id).first()
        if indb:
            raise ProductExistsException()

        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ProductSchema.from_orm(db_product)

    @classmethod
    def update(cls, db: Session, product_id: str, product: ProductSchema) -> ProductSchema:
        db_product = db.query(Product).filter(
            Product.id == product_id).first()
        if db_product is None:
            raise ProductNotFoundException()

        if product.name is not None:
            db_product.name = product.name
        if product.price is not None:
            db_product.price = product.price
        db.commit()
        db.refresh(db_product)

        return ProductSchema.from_orm(db_product)

    @classmethod
    def delete(cls, db: Session, product_id: str) -> None:
        db_product = db.query(Product).filter(
            Product.id == product_id).first()
        if db_product is None:
            raise ProductNotFoundException()
        db.delete(db_product)
        db.commit()
