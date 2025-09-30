import json
import asyncio
from app.crud import create_product
from app.models import Product

async def fill():
    with open("test_products.json") as f:
        data = json.load(f)
        for item in data:
            await create_product(Product(**item))

if __name__ == "__main__":
    asyncio.run(fill())
