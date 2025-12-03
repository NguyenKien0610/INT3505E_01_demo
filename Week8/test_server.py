"""
Unit Tests - Python version of server.test.js (Jest)
Sử dụng pytest và httpx để test FastAPI app
"""
import pytest
from fastapi.testclient import TestClient
from app import app, products

# Reset products trước mỗi test
@pytest.fixture(autouse=True)
def reset_products():
    global products
    products.clear()
    products.extend([
        {"id": 1, "name": "Book", "price": 10},
        {"id": 2, "name": "Pen", "price": 2},
        {"id": 3, "name": "Notebook", "price": 5},
        {"id": 4, "name": "Eraser", "price": 1},
        {"id": 5, "name": "Highlighter", "price": 3}
    ])

client = TestClient(app)

class TestProductAPI:
    """Product API Unit Tests"""
    
    created_id = None
    
    def test_get_all_products(self):
        """GET /products - should return all products"""
        res = client.get("/products")
        assert res.status_code == 200
        assert len(res.json()) > 0
    
    def test_get_product_by_id(self):
        """GET /products/1 - should return product with id=1"""
        res = client.get("/products/1")
        assert res.status_code == 200
        assert res.json()["name"] == "Book"
    
    def test_create_product(self):
        """POST /products - should create a new product"""
        res = client.post("/products", json={"name": "UnitTestProduct", "price": 99})
        assert res.status_code == 201
        assert "id" in res.json()
        TestProductAPI.created_id = res.json()["id"]
    
    def test_update_product(self):
        """PUT /products/:id - should update product info"""
        # Tạo product trước
        res = client.post("/products", json={"name": "ToUpdate", "price": 50})
        product_id = res.json()["id"]
        
        # Update
        res = client.put(f"/products/{product_id}", json={"price": 120})
        assert res.status_code == 200
        assert res.json()["price"] == 120
    
    def test_delete_product(self):
        """DELETE /products/:id - should delete product"""
        # Tạo product trước
        res = client.post("/products", json={"name": "ToDelete", "price": 30})
        product_id = res.json()["id"]
        
        # Delete
        res = client.delete(f"/products/{product_id}")
        assert res.status_code == 204
    
    def test_get_product_not_found(self):
        """GET /products/999999 - should return 404"""
        res = client.get("/products/999999")
        assert res.status_code == 404


# Chạy tests nếu file được chạy trực tiếp
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
