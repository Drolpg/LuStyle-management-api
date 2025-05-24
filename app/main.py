from fastapi import FastAPI
from app.api import auth, clients, products, orders

# (temporario para testar)

# from app.core.database import Base, engine
# from app.models import user, client, product, order  # noqa: F401

# Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"message": "API Lu Estilo esta online!"}
