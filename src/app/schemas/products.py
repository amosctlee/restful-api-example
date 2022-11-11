from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: str
    name: str
    price: int

    class Config:
        orm_mode = True
