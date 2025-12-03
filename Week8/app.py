from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI()

# Data model
class ProductCreate(BaseModel):
    name: str
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

# In-memory database
products = [
    {"id": 1, "name": "Book", "price": 10},
    {"id": 2, "name": "Pen", "price": 2},
    {"id": 3, "name": "Notebook", "price": 5},
    {"id": 4, "name": "Eraser", "price": 1},
    {"id": 5, "name": "Highlighter", "price": 3}
]

# GET all products
@app.get("/products")
def get_products():
    return products

# GET product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product

# POST create new product
@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    new_product = {
        "id": int(time.time() * 1000),
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return new_product

# PUT update product
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    index = next((i for i, p in enumerate(products) if p["id"] == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    if product.name is not None:
        products[index]["name"] = product.name
    if product.price is not None:
        products[index]["price"] = product.price
    
    return products[index]

# DELETE product
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    global products
    original_len = len(products)
    products = [p for p in products if p["id"] != product_id]
    if len(products) == original_len:
        raise HTTPException(status_code=404, detail="Not found")
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    print("✅ Server running on http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=3000)
