# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.products_api_base import BaseProductsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.product import Product
from openapi_server.models.product_create import ProductCreate
from openapi_server.models.product_partial import ProductPartial
from openapi_server.models.product_update import ProductUpdate


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/products",
    responses={
        200: {"model": List[Product], "description": "OK"},
    },
    tags=["Products"],
    summary="List products",
    response_model_by_alias=True,
)
async def list_products(
    q: Annotated[Optional[StrictStr], Field(description="Search by name substring")] = Query(None, description="Search by name substring", alias="q"),
) -> List[Product]:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().list_products(q)


@router.post(
    "/products",
    responses={
        201: {"model": Product, "description": "Created"},
    },
    tags=["Products"],
    summary="Create product",
    response_model_by_alias=True,
)
async def create_product(
    product_create: ProductCreate = Body(None, description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().create_product(product_create)


@router.get(
    "/products/{id}",
    responses={
        200: {"model": Product, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["Products"],
    summary="Get product by id",
    response_model_by_alias=True,
)
async def get_product(
    id: StrictStr = Path(..., description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().get_product(id)


@router.put(
    "/products/{id}",
    responses={
        200: {"model": Product, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["Products"],
    summary="Replace product",
    response_model_by_alias=True,
)
async def replace_product(
    id: StrictStr = Path(..., description=""),
    product_update: ProductUpdate = Body(None, description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().replace_product(id, product_update)


@router.delete(
    "/products/{id}",
    responses={
        204: {"description": "No Content"},
        404: {"description": "Not Found"},
    },
    tags=["Products"],
    summary="Delete product",
    response_model_by_alias=True,
)
async def delete_product(
    id: StrictStr = Path(..., description=""),
) -> None:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().delete_product(id)


@router.patch(
    "/products/{id}",
    responses={
        200: {"model": Product, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["Products"],
    summary="Update partial product",
    response_model_by_alias=True,
)
async def update_product(
    id: StrictStr = Path(..., description=""),
    product_partial: ProductPartial = Body(None, description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().update_product(id, product_partial)
