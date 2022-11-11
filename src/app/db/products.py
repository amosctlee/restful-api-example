
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
        return db_product

    @classmethod
    def list(cls, db: Session, limit: int, offset: int) -> List[ProductSchema]:
        return db.query(Product).limit(limit).offset(offset).all()

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
        return db_product

    @classmethod
    def update(cls, db: Session, product_id: str, product: ProductSchema) -> None:
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

        return db_product

    @classmethod
    def delete(cls, db: Session, product_id: str) -> None:
        db_product = db.query(Product).filter(
            Product.id == product_id).first()
        if db_product is None:
            raise ProductNotFoundException()
        db.delete(db_product)
        db.commit()
