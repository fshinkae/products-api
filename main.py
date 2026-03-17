from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine
from app.models.product import Product
from app.views.product_view import ProductCreate, ProductUpdate, ProductResponse
from app.controllers import product_controller

Product.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products API",
    description="CRUD de produtos com bugs intencionais documentados",
    version="1.0.0",
)


@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_controller.create_product(db, product)


@app.get("/products", response_model=List[ProductResponse])
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return product_controller.get_products(db, page=page, page_size=page_size)


@app.get("/products/search", response_model=List[dict])
def search_products(name: str = Query(...), db: Session = Depends(get_db)):
    results = product_controller.search_products_by_name(db, name)
    return [dict(row._mapping) for row in results]


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_controller.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = product_controller.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = product_controller.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}
