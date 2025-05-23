
from flask import Blueprint,request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED

from app.models.Product import Product
from app.extensions import db


#Product blueprint
products = Blueprint('products', __name__,url_prefix= '/api/v1/products')


@products.route('/products', methods=['POST'])

# Creating new product
def create_product():
    data = request.get_json()
    print("Received data:", data)

    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

# Validation
    if not name or not price:
        return jsonify({"error": "Product name and price are required."}), HTTP_400_BAD_REQUEST

    try:
        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

    return jsonify({
        "message": "Product created successfully.",
        "product": {
            "id": new_product.product_id,
            "product_name": new_product.name,
            "category_id": new_product.category_id,
            "image":new_product.image,
            "description": new_product.description
        }
    }), HTTP_201_CREATED



# Retrieve all products
@products.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()

    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "product_name": product.name,
            "category_id": product.category_id,
            "image":product.image,
            "description": product.description
        })

    return jsonify({"products": products_list}), HTTP_200_OK 

# Update a product by ID
@products.route('/update/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()
        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found."}),HTTP_404_NOT_FOUND

        product.product_name = data.get('product_name', product.product_name)
        product.category_id = data.get('category_id', product.category_id)
        product.description = data.get('description', product.description)
        product.image = data.get('image', product.image)

        db.session.commit()

        return jsonify({
            "message": f"Product with ID {id} updated successfully.",
            "product": {
                "id": product.id,
                "product_name": product.product_name,
                "category_id": product.category_id, 
                "description": product.description,
                "image":product.image,
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete a product by ID
@products.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found."}), HTTP_404_NOT_FOUND

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": f"Product with ID {id} deleted successfully."}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR