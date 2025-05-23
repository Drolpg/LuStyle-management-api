import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.database import get_db  # noqa: F401
from app.models import user, client, product, order  # noqa: F401
from app.core.security import create_access_token


# Cria um usuário e retorna um token válido
@pytest.fixture
def auth_header(db: Session):
    fake_user = user.User(email="admin@example.com", hashed_password="123")
    db.add(fake_user)
    db.commit()
    token = create_access_token({"sub": fake_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_order(auth_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Cria client e product antes
        client_data = {
            "name": "Cliente Teste",
            "cpf": "12345678900",
            "email": "cliente@teste.com",
            "phone_number": "11999999999",
        }
        product_data = {
            "name": "Produto Teste",
            "price": 10.0,
            "description": "Descrição",
            "in_stock": 100,
        }

        client_resp = await ac.post(
            "/clients/", json=client_data, headers=auth_header)
        product_resp = await ac.post(
            "/products/", json=product_data, headers=auth_header
        )

        order_data = {
            "client_id": client_resp.json()["id"],
            "product_id": product_resp.json()["id"],
            "quantity": 2,
        }

        response = await ac.post(
            "/orders/", json=order_data, headers=auth_header)
        assert response.status_code == 200
        assert response.json()["quantity"] == 2


@pytest.mark.asyncio
async def test_list_orders(auth_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/orders/", headers=auth_header)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_order(auth_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/orders/1", headers=auth_header)
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_delete_order(auth_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Primeiro cria um pedido
        client_resp = await ac.get("/clients/", headers=auth_header)
        product_resp = await ac.get("/products/", headers=auth_header)

        if not client_resp.json() or not product_resp.json():
            pytest.skip(
                "Cliente ou produto não disponível para deletar pedido")

        order_data = {
            "client_id": client_resp.json()[0]["id"],
            "product_id": product_resp.json()[0]["id"],
            "quantity": 1,
        }
        create_resp = await ac.post(
            "/orders/", json=order_data, headers=auth_header)
        order_id = create_resp.json()["id"]

        # Agora deleta
        delete_resp = await ac.delete(
            f"/orders/{order_id}", headers=auth_header)
        assert delete_resp.status_code == 200
