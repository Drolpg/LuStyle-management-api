from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    phone_number: str


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    registration_date: datetime

    class Config:
        orm_mode = True
