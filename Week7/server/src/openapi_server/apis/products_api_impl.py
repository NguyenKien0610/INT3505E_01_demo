# coding: utf-8
from typing import List, Optional
from datetime import datetime
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

from openapi_server.apis.products_api_base import BaseProductsApi
from openapi_server.models.product import Product
from openapi_server.models.product_create import ProductCreate
from openapi_server.models.product_update import ProductUpdate
from openapi_server.models.product_partial import ProductPartial


load_dotenv()

# Environment variables
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "product_db")


def _get_client() -> AsyncIOMotorClient:
    if not MONGODB_URL:
        raise RuntimeError("MONGODB_URL not set in environment")
    return AsyncIOMotorClient(MONGODB_URL)


class ProductsApiImpl(BaseProductsApi):
    """Mongo-backed implementation of products API."""

    def __init__(self):
        self._client = _get_client()
        self._db = self._client[MONGODB_DATABASE]
        self._col = self._db["products"]

    async def list_products(self, q: Optional[str]) -> List[Product]:
        query = {}
        if q:
            # simple case-insensitive substring search on name
            query = {"name": {"$regex": q, "$options": "i"}}

        docs = []
        cursor = self._col.find(query).sort("_id", 1)
        async for d in cursor:
            docs.append(_doc_to_product(d))
        return docs

    async def create_product(self, product_create: ProductCreate) -> Product:
        now = datetime.utcnow()
        doc = product_create.model_dump()
        doc.update({"createdAt": now, "updatedAt": now})
        res = await self._col.insert_one(doc)
        inserted = await self._col.find_one({"_id": res.inserted_id})
        return _doc_to_product(inserted)

    async def get_product(self, id: str) -> Product:
        try:
            oid = ObjectId(id)
        except InvalidId:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        doc = await self._col.find_one({"_id": oid})
        if not doc:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        return _doc_to_product(doc)

    async def replace_product(self, id: str, product_update: ProductUpdate) -> Product:
        now = datetime.utcnow()
        update_doc = product_update.model_dump()
        update_doc.update({"updatedAt": now, "createdAt": update_doc.get("createdAt")})
        try:
            oid = ObjectId(id)
        except InvalidId:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        res = await self._col.replace_one({"_id": oid}, update_doc)
        if res.matched_count == 0:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        doc = await self._col.find_one({"_id": ObjectId(id)})
        return _doc_to_product(doc)

    async def delete_product(self, id: str) -> None:
        try:
            oid = ObjectId(id)
        except InvalidId:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        res = await self._col.delete_one({"_id": oid})
        if res.deleted_count == 0:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        return None

    async def update_product(self, id: str, product_partial: ProductPartial) -> Product:
        now = datetime.utcnow()
        update_fields = product_partial.model_dump(exclude_none=True)
        if not update_fields:
            # nothing to update, return current
            try:
                oid = ObjectId(id)
            except InvalidId:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Not Found")
            doc = await self._col.find_one({"_id": oid})
            if not doc:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Not Found")
            return _doc_to_product(doc)
        update_fields["updatedAt"] = now
        try:
            oid = ObjectId(id)
        except InvalidId:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        res = await self._col.update_one({"_id": oid}, {"$set": update_fields})
        if res.matched_count == 0:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not Found")
        doc = await self._col.find_one({"_id": oid})
        return _doc_to_product(doc)


def _doc_to_product(doc: dict) -> Product:
    # convert Mongo document to Product model. Map _id to id and handle datetime aliases
    out = {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "price": doc.get("price"),
        "description": doc.get("description"),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
    }
    return Product.model_validate(out)
