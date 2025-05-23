from flask import Blueprint,request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED

from app.models.Customer import Customer
from app.extensions import db


#Customer blueprint
customers = Blueprint('customers', __name__,url_prefix= '/api/v1/customers')


@customers.route('/customers', methods=['POST'])

# Creating new customer
def create_product():
    data = request.get_json()
    print("Received data:", data)

    name = data.get('name')
    customer_id = data.get('product_id')
    address = data.get('address')
    image = data.get('image')

# Validation
    if not name or not customer_id:
        return jsonify({"error": "Product name andcustomer_id are required."}), HTTP_400_BAD_REQUEST

    try:
        new_customer = Customer(name=name, customer_id=customer_id, address=address)
        db.session.add(new_customer)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

    return jsonify({
        "message": "customer created successfully.",
        "customer": {
            "id": new_customer.id,
            "customer_name": new_customer.name,
            "product_id": new_customer.product_id,
            "image":new_customer.image,
            "address": new_customer.address
        }
    }), HTTP_201_CREATED

