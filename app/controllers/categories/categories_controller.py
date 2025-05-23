from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
from app.extensions import db
from app.models.Category import Category


#authors blueprint
categories_bp = Blueprint('categories_bp', __name__, url_prefix ='/api/v1/categories_bp')


# Creating a category
@categories_bp.route('/create', methods=['POST'])

def createBook():
    data = request.json
    product_id  = data.get('product_id')
    created_at = data.get('created_at')
   

    # Validations
    if not product_id:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if Category.query.filter_by(product_id=product_id) is not None:
        return jsonify({"error": "Book title and author id already in use"}), HTTP_409_CONFLICT

    try:
        # Creating a new category
        new_category = Category (
            
            product_id =product_id,
            created_at=created_at
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            'message': f"{product_id} has been successfully created",
            'category': {
                "id": new_category.id,
                "product_id": new_category.product_id,
                "created_at": new_category.created_at,
                "product": {
                    'product_id': new_category.product.product_id,
                    'category_id': new_category.product.category_id,
                    'description': new_category.product.description,
                    'created_at': new_category.product.created_at
                },
                
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR