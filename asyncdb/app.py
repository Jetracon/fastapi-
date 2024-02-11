from databases import Database
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import ProductModel
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:!_zubast444ik-_9204924-MYSQL24242_242424zubastik_!@localhost/hillelfastapi"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
app = FastAPI()
Base = declarative_base()

database = Database(SQLALCHEMY_DATABASE_URL)


# Dependency to get async database session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_product(db: AsyncSession, product_payload: ProductModel) -> ProductModel:
    product = ProductModel(**product_payload.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def get_product_by_id(db: AsyncSession, product_id: int) -> ProductModel:
    result = await db.execute(select(ProductModel).filter(ProductModel.id == product_id))
    product = result.scalars().first()
    return product

async def update_product(db: AsyncSession, product_id: int, product_payload: ProductModel) -> ProductModel:
    db_product = await get_product_by_id(db, product_id)

    if db_product:
        for key, value in product_payload.dict().items():
            setattr(db_product, key, value)

        await db.commit()
        await db.refresh(db_product)

    return db_product

async def delete_product(db: AsyncSession, product_id: int) -> ProductModel:
    db_product = await get_product_by_id(db, product_id)

    if db_product:
        db.delete(db_product)
        await db.commit()

    return db_product

@app.post("/products", response_model=ProductModel)
async def create_product_endpoint(product_payload: ProductModel, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product_payload)

@app.get("/products/{product_id}", response_model=ProductModel)
async def read_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductModel)
async def update_product_endpoint(product_id: int, product_payload: ProductModel, db: AsyncSession = Depends(get_db)):
    updated_product = await update_product(db, product_id, product_payload)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}", response_model=ProductModel)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted_product = await delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product