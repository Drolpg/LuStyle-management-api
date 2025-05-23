from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    in_stock: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
