"""
Testes para deleção de produtos.
"""


def _create(client, name="Produto", price=10.0, stock=5):
    return client.post("/products", json={"name": name, "price": price, "stock": stock}).json()


def test_delete_product_success(client):
    created = _create(client)
    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Produto deletado com sucesso"


def test_delete_product_not_found(client):
    response = client.delete("/products/9999")
    assert response.status_code == 404


def test_delete_product_cannot_be_fetched_after(client):
    created = _create(client)
    client.delete(f"/products/{created['id']}")
    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 404


def test_delete_product_twice(client):
    created = _create(client)
    client.delete(f"/products/{created['id']}")
    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 404
