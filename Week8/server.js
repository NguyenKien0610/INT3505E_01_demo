const express = require("express");
const app = express();
app.use(express.json());

let products = [
  { id: 1, name: "Book", price: 10 },
  { id: 2, name: "Pen", price: 2 }
];

app.get("/products", (req, res) => res.json(products));

app.get("/products/:id", (req, res) => {
  const product = products.find(p => p.id == req.params.id);
  product ? res.json(product) : res.status(404).send("Not found");
});

app.post("/products", (req, res) => {
  const newProduct = { id: Date.now(), ...req.body };
  products.push(newProduct);
  res.status(201).json(newProduct);
});

app.put("/products/:id", (req, res) => {
  const index = products.findIndex(p => p.id == req.params.id);
  if (index === -1) return res.status(404).send("Not found");
  products[index] = { ...products[index], ...req.body };
  res.json(products[index]);
});

app.delete("/products/:id", (req, res) => {
  products = products.filter(p => p.id != req.params.id);
  res.sendStatus(204);
});

app.listen(3000, () => console.log("✅ Server running on http://localhost:3000"));
