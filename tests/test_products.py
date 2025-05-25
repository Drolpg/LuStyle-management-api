import uuid


def test_create_product(authenticated_client):
    unique_suffix = uuid.uuid4().hex[:10]
    response = authenticated_client.post(
        "/products/",
        json={
            "name": f"Camiseta Básica {unique_suffix}",
            "price": 49.90,
            "description": "Camiseta algodão branca",
            "in_stock": 100,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == f"Camiseta Básica {unique_suffix}"
    assert data["price"] == 49.90
    assert "id" in data


def test_list_products(authenticated_client):
    response = authenticated_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
