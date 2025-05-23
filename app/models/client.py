from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
