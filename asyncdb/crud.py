from sqlalchemy.orm import Session
from . import models
from pydantic_models import ProductPayload
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, db_product: models.Product, product_update: ProductPayload):
    db_product.name = product_update.name
    db_product.is_18_plus = product_update.is_18_plus
    db_product.price = product_update.price
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: models.Product):
    db.delete(db_product)
    db.commit()