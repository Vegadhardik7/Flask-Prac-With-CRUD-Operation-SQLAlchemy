import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify

# Init App
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description', 'price', 'qty')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_Product():
    print(f"TAKING VALUES FROM THE USER COLUMNS")
    data = request.json
    name = data['name']
    print(f"NAME: {name}")
    description = data['description']
    price = data['price']
    qty = data['qty']

    new_prod = Product(name, description, price, qty)
    print(f"THIS IS DATA: {new_prod}")
    db.session.add(new_prod)
    db.session.commit()

    return product_schema.jsonify(new_prod)

# Get all single product
@app.route("/product/<id>",methods=['GET'])
def get_single_Product(id):
    prod = Product.query.get(id)
    result = product_schema.jsonify(prod)
    return result

# Get all products
@app.route("/product",methods=['GET'])
def get_all_Products():
    all_prod = Product.query.all()
    result = products_schema.dump(all_prod)
    return jsonify(result)

# ------------------------------------------------------------------------

# Update Product
@app.route('/product/<id>', methods=['PUT'])
def Update_Product(id):
    
    product = Product.query.get(id)

    data = request.json
    name = data['name']
    print(f"NAME: {name}")
    description = data['description']
    price = data['price']
    qty = data['qty']

    product.name = name
    product.price = price
    product.description = description
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# -----------------------------------------------------------------------------

# delete the product
@app.route("/product/<id>",methods=['DELETE'])
def delete_single_Product(id):
    prod = Product.query.get(id)    
    db.session.delete(prod)
    db.session.commit()
    return product_schema.jsonify(prod)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
