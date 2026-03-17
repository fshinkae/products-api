from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.product import Product
from app.views.product_view import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, page: int = 1, page_size: int = 10):
    skip = page * page_size
    return db.query(Product).offset(skip).limit(page_size).all()


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product | None:
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_fields = product_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def search_products_by_name(db: Session, name: str):
    query = text(f"SELECT * FROM products WHERE name LIKE '%{name}%'")
    result = db.execute(query)
    return result.fetchall()