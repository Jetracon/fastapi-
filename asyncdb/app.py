from http.client import HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status, Depends
# declarative_base class, Column, Integer and String
# will all be used for the race_car table model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
# Session will be used together wiith create_engine
# for the connection session
from sqlalchemy.orm import Session
from pydantic_models import ProductPayload
from . import crud, models, database
# my database is on the same machine
# you should change the localhost with the IP of
# your database
DB_HOST = "localhost"
# the database we created in the previous article
# https://keepforyourself.com/databases/mysql/how-to-install-mysql-on-your-linux-system/
DATABASE = "playground"

engine = create_engine(f"mysql+pymysql://root:!_zubast444ik-_9204924-MYSQL24242_242424zubastik_!@{DB_HOST}/{DATABASE}")
DBSession = Session(engine)

DB_BASE_ORM = declarative_base()

app = FastAPI(
    title="Example-02-CRUD-part-2",
    description="keep-4-yourself-example-03",
)

@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: ProductPayload, db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return crud.update_product(db, db_product, product_update)


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.delete_product(db, db_product)
    return {"message": "Product successfully deleted"}


@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product