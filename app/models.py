from typing import Optional
from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId, AsyncAbstractRepository
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os


class Product(BaseModel):
    id: Optional[PydanticObjectId] = None
    sku: str
    name: str
    image_url: list[str]
    specification_url: Optional[str]


class ProductRepository(AsyncAbstractRepository[Product]):
    class Meta:
        collection_name = "products"


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["product_db"]
repo = ProductRepository(database=db)
