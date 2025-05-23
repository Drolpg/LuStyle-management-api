def test_create_client(client):
    response = client.post(
        "/clients/",
        json={
            "name": "João da Silva",
            "email": "joao@example.com",
            "cpf": "12345678900",
            "phone_number": "11999999999",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "João da Silva"
    assert data["email"] == "joao@example.com"
    assert "id" in data


def test_list_clients(client):
    response = client.get("/clients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
