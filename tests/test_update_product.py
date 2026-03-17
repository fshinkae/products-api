"""
Testes para atualização de produtos.
"""


def _create(client, name="Produto", price=10.0, stock=5):
    return client.post("/products", json={"name": name, "price": price, "stock": stock}).json()


def test_update_product_name(client):
    created = _create(client, name="Antigo")
    response = client.put(f"/products/{created['id']}", json={"name": "Novo"})
    assert response.status_code == 200
    assert response.json()["name"] == "Novo"


def test_update_product_price(client):
    created = _create(client, price=100.0)
    response = client.put(f"/products/{created['id']}", json={"price": 200.0})
    assert response.status_code == 200
    assert response.json()["price"] == 200.0


def test_update_product_stock(client):
    created = _create(client, stock=10)
    response = client.put(f"/products/{created['id']}", json={"stock": 99})
    assert response.status_code == 200
    assert response.json()["stock"] == 99


def test_update_product_partial(client):
    created = _create(client, name="Original", price=50.0, stock=3)
    response = client.put(f"/products/{created['id']}", json={"price": 75.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Original"   # não alterado
    assert data["price"] == 75.0        # alterado
    assert data["stock"] == 3           # não alterado


def test_update_product_not_found(client):
    response = client.put("/products/9999", json={"name": "X"})
    assert response.status_code == 404


def test_update_product_empty_body(client):
    created = _create(client, name="Inalterado")
    response = client.put(f"/products/{created['id']}", json={})
    assert response.status_code == 200
    assert response.json()["name"] == "Inalterado"
