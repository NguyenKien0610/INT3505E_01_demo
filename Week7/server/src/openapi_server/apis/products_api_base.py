# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.product import Product
from openapi_server.models.product_create import ProductCreate
from openapi_server.models.product_partial import ProductPartial
from openapi_server.models.product_update import ProductUpdate


class BaseProductsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProductsApi.subclasses = BaseProductsApi.subclasses + (cls,)
    async def list_products(
        self,
        q: Annotated[Optional[StrictStr], Field(description="Search by name substring")],
    ) -> List[Product]:
        ...


    async def create_product(
        self,
        product_create: ProductCreate,
    ) -> Product:
        ...


    async def get_product(
        self,
        id: StrictStr,
    ) -> Product:
        ...


    async def replace_product(
        self,
        id: StrictStr,
        product_update: ProductUpdate,
    ) -> Product:
        ...


    async def delete_product(
        self,
        id: StrictStr,
    ) -> None:
        ...


    async def update_product(
        self,
        id: StrictStr,
        product_partial: ProductPartial,
    ) -> Product:
        ...
