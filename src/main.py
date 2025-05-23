from fastapi import FastAPI
from controllers import clients_controllers


app = FastAPI(
    title="API Catalogo de clientes",
    description="API para gerenciamento e catalogar clientes",
    version="0.0.1",
)

app.include_router(clients_controllers.router)
