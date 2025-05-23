from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/lustyle"
)
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro na conexão:", e)
