from app.core.database import SessionLocal
from app.models.client import Client
import uuid


def create_test_client_db_entry():
    """Cria um cliente no banco de dados com dados únicos para testes."""
    db = SessionLocal()
    try:
        unique_suffix = uuid.uuid4().hex[:10]
        client = Client(
            name=f"Cliente Teste DB {unique_suffix}",
            email=f"teste.db.{unique_suffix}@email.com",
            cpf=f"111222333{unique_suffix[:2]}",
            phone_number=f"9999999{unique_suffix[:4]}",
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    finally:
        db.close()


def test_create_client(authenticated_client):
    response = authenticated_client.post(
        "/clients/",
        json={
            "name": "João da Silva",
            "email": f"joao.client.{uuid.uuid4().hex[:10]}@example.com",
            "cpf": f"123456789{uuid.uuid4().hex[:2]}",
            "phone_number": f"119999999{uuid.uuid4().hex[:4]}",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "João da Silva"
    assert "id" in data


def test_list_clients(authenticated_client):
    response = authenticated_client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_client_by_id(authenticated_client):
    client_db_entry = create_test_client_db_entry()
    response = authenticated_client.get(f"/clients/{client_db_entry.id}")
    assert response.status_code == 200
    assert response.json()["id"] == client_db_entry.id


def test_update_client(authenticated_client):
    client_db_entry = create_test_client_db_entry()
    response = authenticated_client.put(
        f"/clients/{client_db_entry.id}",
        json={
            "name": "Cliente Atualizado",
            "email": f"atualizado.{uuid.uuid4().hex[:10]}@email.com",
            "cpf": client_db_entry.cpf,
            "phone_number": f"8888888{uuid.uuid4().hex[:4]}",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Cliente Atualizado"


def test_delete_client(authenticated_client):
    client_db_entry = create_test_client_db_entry()
    response = authenticated_client.delete(f"/clients/{client_db_entry.id}")

    assert response.status_code == 204

    response = authenticated_client.get(f"/clients/{client_db_entry.id}")
    assert response.status_code == 404
