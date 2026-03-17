def _create(client, name, price=10.0, stock=5):
    return client.post("/products", json={"name": name, "price": price, "stock": stock}).json()


def test_search_product_found(client):
    _create(client, name="Notebook Gamer")
    response = client.get("/products/search?name=Notebook")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Notebook Gamer"


def test_search_product_partial_match(client):
    _create(client, name="Mouse USB")
    _create(client, name="Mouse Bluetooth")
    response = client.get("/products/search?name=Mouse")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_search_product_no_results(client):
    _create(client, name="Teclado")
    response = client.get("/products/search?name=Monitor")
    assert response.status_code == 200
    assert response.json() == []


def test_search_product_missing_param(client):
    response = client.get("/products/search")
    assert response.status_code == 422


def test_search_case_sensitive(client):
    _create(client, name="Headset")
    response = client.get("/products/search?name=headset")
    assert response.status_code == 200


def test_search_returns_all_with_special_input(client):
    _create(client, name="Produto A")
    _create(client, name="Produto B")
    _create(client, name="Produto C")

    response = client.get("/products/search?name=' OR '1'='1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_search_with_sql_comment_input(client):
    _create(client, name="Secreto")
    _create(client, name="Público")

    response = client.get("/products/search?name=Nada' OR 1=1 --")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
