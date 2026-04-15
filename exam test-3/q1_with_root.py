#make me a python REST API using flask for a e-commerce product inventory with the following endpoints: Add a product (name, price, quantity) ; Get all products; Get a product by id; Update a product by id; Delete a product by id. at the end i want to Show sample JSON request and response 
from flask import Flask, request, jsonify

from q1data import sample_products

app = Flask(__name__)
products = [product.copy() for product in sample_products]
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    products.append(product)
    return jsonify(product), 201
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product["name"] = data.get("name", product["name"])
    product["price"] = data.get("price", product["price"])
    product["quantity"] = data.get("quantity", product["quantity"])

    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return jsonify({"message": "Product deleted"})

@app.route('/')
def home():
    return jsonify({"message": "API is running"})
