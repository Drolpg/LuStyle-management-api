import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/lustyle"
)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Conexão OK")
except Exception as e:

    print("Erro:", str(e).encode("utf-8", errors="replace").decode("utf-8"))
