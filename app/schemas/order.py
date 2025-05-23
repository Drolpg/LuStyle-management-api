from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    client_id: int
    product_id: int
    quantity: int


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
