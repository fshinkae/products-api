def test_create_product_success(client):
    payload = {"name": "Notebook", "price": 3500.0, "stock": 10}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Notebook"
    assert data["price"] == 3500.0
    assert data["stock"] == 10


def test_create_product_with_description(client):
    payload = {"name": "Mouse", "description": "Mouse sem fio", "price": 150.0, "stock": 50}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    assert response.json()["description"] == "Mouse sem fio"


def test_create_product_missing_name(client):
    payload = {"price": 100.0, "stock": 5}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_missing_price(client):
    payload = {"name": "Teclado", "stock": 5}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_missing_stock(client):
    payload = {"name": "Monitor", "price": 1200.0}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_negative_price(client):
    payload = {"name": "Produto Inválido", "price": -50.0, "stock": 10}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    assert response.json()["price"] == -50.0


def test_create_product_negative_stock(client):
    payload = {"name": "Produto Inválido", "price": 10.0, "stock": -5}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    assert response.json()["stock"] == -5


def test_create_product_status_code(client):
    payload = {"name": "Headset", "price": 250.0, "stock": 20}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    assert response.status_code != 201
