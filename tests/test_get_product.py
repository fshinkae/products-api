def _create(client, name="Produto", price=10.0, stock=5):
    return client.post("/products", json={"name": name, "price": price, "stock": stock}).json()


def test_get_product_success(client):
    created = _create(client, name="Caneta")
    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Caneta"


def test_get_product_not_found(client):
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_get_product_invalid_id(client):
    response = client.get("/products/abc")
    assert response.status_code == 422


def test_list_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products_with_items(client):
    _create(client, name="Item A")
    _create(client, name="Item B")
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_list_products_page1_empty(client):
    for i in range(5):
        _create(client, name=f"Produto {i}", price=float(i + 1), stock=i)

    response = client.get("/products?page=1&page_size=10")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products_pagination_offset(client):
    _create(client, name="Primeiro")
    _create(client, name="Segundo")
    _create(client, name="Terceiro")

    response = client.get("/products?page=1&page_size=2")
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Terceiro"
