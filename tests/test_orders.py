import uuid


def test_create_order(authenticated_client):
    unique_suffix_client = uuid.uuid4().hex[:10]
    client_data = {
        "name": "Maria da Moda",
        "email": f"maria.order.{unique_suffix_client}@example.com",
        "cpf": f"987654321{unique_suffix_client[:2]}",
        "phone_number": f"118888888{unique_suffix_client[:4]}",
    }
    client_response = authenticated_client.post("/clients/", json=client_data)
    assert (
        client_response.status_code == 200
    ), f"Failed to create client: {client_response.text}"
    client_id = client_response.json()["id"]

    unique_suffix_product = uuid.uuid4().hex[:10]
    product_data = {
        "name": f"Calça Jeans {unique_suffix_product}",
        "price": 99.90,
        "description": "Calça jeans azul clara",
        "in_stock": 50,
    }
    product_response = authenticated_client.post(
        "/products/", json=product_data)
    assert (
        product_response.status_code == 200
    ), f"Failed to create product: {product_response.text}"
    product_id = product_response.json()["id"]

    order_response = authenticated_client.post(
        "/orders/",
        json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1,
        },
    )
    assert (
        order_response.status_code == 200
    ), f"Failed to create order: {order_response.text}"
    data = order_response.json()
    assert data["client_id"] == client_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 1
    assert "id" in data


def test_list_orders(authenticated_client):
    response = authenticated_client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
