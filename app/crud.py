from app.models import db, Product

collection = db["products"]

async def create_product(product: Product):
    await collection.insert_one(product.model_dump())
