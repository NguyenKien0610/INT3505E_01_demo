# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.product import Product  # noqa: F401
from openapi_server.models.product_create import ProductCreate  # noqa: F401
from openapi_server.models.product_partial import ProductPartial  # noqa: F401
from openapi_server.models.product_update import ProductUpdate  # noqa: F401


def test_list_products(client: TestClient):
    """Test case for list_products

    List products
    """
    params = [("q", 'q_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_product(client: TestClient):
    """Test case for create_product

    Create product
    """
    product_create = {"price":0.8008281904610115,"name":"name","description":"description"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/products",
    #    headers=headers,
    #    json=product_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_product(client: TestClient):
    """Test case for get_product

    Get product by id
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_replace_product(client: TestClient):
    """Test case for replace_product

    Replace product
    """
    product_update = {"price":0.8008281904610115,"name":"name","description":"description"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/products/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=product_update,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_product(client: TestClient):
    """Test case for delete_product

    Delete product
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/products/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_product(client: TestClient):
    """Test case for update_product

    Update partial product
    """
    product_partial = {"price":0.8008281904610115,"name":"name","description":"description"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/products/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=product_partial,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

