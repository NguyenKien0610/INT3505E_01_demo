# coding: utf-8
from typing import List, Optional
from datetime import datetime
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

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

    def _id_filter(self, iid: int) -> dict:
        """Return a Mongo filter that matches documents whose `id` is the given
        integer or the string representation (handles mixed types in DB).
        """
        return {"$or": [{"id": iid}, {"id": str(iid)}]}
    async def list_products(self, q: Optional[str]) -> List[Product]:
        query = {}
        if q:
            # simple case-insensitive substring search on name
            query = {"name": {"$regex": q, "$options": "i"}}

        docs = []
        cursor = self._col.find(query).sort("id", 1)
        async for d in cursor:
            docs.append(_doc_to_product(d))
        return docs

    async def create_product(self, product_create: ProductCreate) -> Product:
        now = datetime.utcnow()
        doc = product_create.model_dump()
        doc.update({"createdAt": now, "updatedAt": now})
        # if client provided a numeric `id`, block when it already exists
        if doc.get("id") is not None:
            try:
                iid = int(doc.get("id"))
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="id must be an integer")
            exists = await self._col.find_one(self._id_filter(iid))
            if exists:
                raise HTTPException(status_code=409, detail="Product with this id already exists")

        # normalize id to integer in the stored document if provided
        if doc.get("id") is not None:
            try:
                doc["id"] = int(doc.get("id"))
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="id must be an integer")

        res = await self._col.insert_one(doc)
        # prefer to find by numeric `id` field if the payload provided one;
        # otherwise fall back to the Mongo-generated _id
        if doc.get("id") is not None:
            inserted = await self._col.find_one(self._id_filter(int(doc.get("id"))))
        else:
            inserted = await self._col.find_one({"_id": res.inserted_id})
        if not inserted:
            raise HTTPException(status_code=500, detail="Failed to retrieve inserted product")
        return _doc_to_product(inserted)

    async def get_product(self, id: str) -> Product:
        # search by numeric `id` field (not Mongo _id)
        try:
            iid = int(id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=404, detail="Not Found")

        doc = await self._col.find_one(self._id_filter(iid))
        if not doc:
            raise HTTPException(status_code=404, detail="Not Found")
        return _doc_to_product(doc)

    async def replace_product(self, id: str, product_update: ProductUpdate) -> Product:
        now = datetime.utcnow()
        update_doc = product_update.model_dump()
        update_doc.update({"updatedAt": now, "createdAt": update_doc.get("createdAt")})
        # replace by numeric `id` field
        try:
            iid = int(id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=404, detail="Not Found")

        # ensure document exists and keep its _id when replacing
        existing = await self._col.find_one(self._id_filter(iid))
        if not existing:
            raise HTTPException(status_code=404, detail="Not Found")

        update_doc["_id"] = existing.get("_id")
        # ensure stored id preserved/normalized
        update_doc["id"] = iid
        res = await self._col.replace_one(self._id_filter(iid), update_doc)
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Not Found")
        doc = await self._col.find_one(self._id_filter(iid))
        if not doc:
            raise HTTPException(status_code=404, detail="Not Found")
        return _doc_to_product(doc)

    async def delete_product(self, id: str) -> None:
        # delete by numeric `id` field
        try:
            iid = int(id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=404, detail="Not Found")

        res = await self._col.delete_one(self._id_filter(iid))
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Not Found")
        return None

    async def update_product(self, id: str, product_partial: ProductPartial) -> Product:
        now = datetime.utcnow()
        update_fields = product_partial.model_dump(exclude_none=True)
        if not update_fields:
            # nothing to update, return current
            try:
                iid = int(id)
            except (ValueError, TypeError):
                raise HTTPException(status_code=404, detail="Not Found")
            doc = await self._col.find_one(self._id_filter(iid))
            if not doc:
                raise HTTPException(status_code=404, detail="Not Found")
            return _doc_to_product(doc)
        update_fields["updatedAt"] = now
        try:
            iid = int(id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=404, detail="Not Found")

        res = await self._col.update_one(self._id_filter(iid), {"$set": update_fields})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Not Found")
        doc = await self._col.find_one(self._id_filter(iid))
        if not doc:
            raise HTTPException(status_code=404, detail="Not Found")
        return _doc_to_product(doc)


def _doc_to_product(doc: dict) -> Product:
    # convert Mongo document to Product model. Map id to id and handle datetime aliases
    out = {
        # Prefer the numeric `id` field when present; otherwise use the Mongo _id
        "id": str(doc.get("id")) if doc.get("id") is not None else str(doc.get("_id")),
        "name": doc.get("name"),
        "price": doc.get("price"),
        "description": doc.get("description"),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
    }
    return Product.model_validate(out)
