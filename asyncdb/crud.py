from sqlalchemy.orm import Session
from models import ProductModel
from pydantic_models import ProductPayload
def get_product(db: Session, product_id: int):
    return db.query(ProductModel.Product).filter(ProductModel.Product.id == product_id).first()

def update_product(db: Session, db_product: ProductModel, product_update: ProductPayload):
    db_product.name = product_update.name
    db_product.is_18_plus = product_update.is_18_plus
    db_product.price = product_update.price
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: ProductModel):
    db.delete(db_product)
    db.commit()