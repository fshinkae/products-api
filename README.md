# Products API

API REST para cadastro de produtos desenvolvida com FastAPI, SQLite e arquitetura MVC.

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Docker

## Estrutura do Projeto

```
products-api/
├── app/
│   ├── controllers/
│   │   └── product_controller.py  # Lógica de negócio
│   ├── models/
│   │   └── product.py             # Modelo de dados
│   └── views/
│       └── product_view.py        # Schemas de entrada e saída
├── tests/
│   ├── conftest.py
│   ├── test_create_product.py
│   ├── test_delete_product.py
│   ├── test_get_product.py
│   ├── test_search_product.py
│   └── test_update_product.py
├── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/products` | Cadastrar produto |
| `GET` | `/products` | Listar produtos (paginado) |
| `GET` | `/products/{id}` | Buscar produto por ID |
| `GET` | `/products/search?name=` | Buscar produtos por nome |
| `PUT` | `/products/{id}` | Atualizar produto |
| `DELETE` | `/products/{id}` | Deletar produto |

## Como Executar

### Com Docker

```bash
docker-compose up --build
```

### Sem Docker

```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar a aplicação
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

Documentação interativa: `http://localhost:8000/docs`

## Testes

```bash
pytest tests/ -v
```

## Exemplos de Uso

### Cadastrar produto

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "description": "Notebook Gamer", "price": 3500.0, "stock": 10}'
```

### Listar produtos

```bash
curl http://localhost:8000/products?page=1&page_size=10
```

### Buscar por nome

```bash
curl http://localhost:8000/products/search?name=Notebook
```

### Atualizar produto

```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 3200.0}'
```

### Deletar produto

```bash
curl -X DELETE http://localhost:8000/products/1
```
