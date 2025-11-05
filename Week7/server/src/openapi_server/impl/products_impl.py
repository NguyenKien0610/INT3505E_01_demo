"""Implementation bridge module.

This module exists so that `openapi_server.apis.products_api` can import
all modules under `openapi_server.impl` and thereby load the concrete
implementation class defined in `openapi_server.apis.products_api_impl`.
"""
from openapi_server.apis.products_api_impl import ProductsApiImpl  # noqa: F401
