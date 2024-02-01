"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, Response
from api.models import db, User, Address, UserAddress, ProductCategory, Promotion, PromotionCategory, Products, ProductItem
from api.models import Variation, VariationOption, ProductConfiguration, PaymentType, UserPaymentMethod, ShoppingCart, ShoppingCartItem
from api.models import OrderStatus, ShippingMethod, ShopOrder, OrderLine, UserReview
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
# from werkzeug.utils import secure_filename

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# @api.route('/upload', methods=['POST'])
# def upload():
#     pic = request.files['pic']

#     if not pic:
#        return 'No image uploaded', 400
    
#     filename = secure_filename(pic.filename)
#     mimetype = pic.mimetype

#     img = Img(img=pic.read(), mimetype=mimetype)
#     db.session.add(img)
#     db.session.commit()

#     return 'img has been uploaded', 200

# @api.route('/get_img/<int:id>', methods=["GET"])
# def get_img(id):
#     img = Img.query.filter_by(id=id).first()
#     if not img:
#         return 'No img with that id', 404
    
#     return Response(img.img, mimetype=img.mimetype)

@api.route("/admin_login", methods=["POST"])
def admin_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
   
    if user is None:
        return jsonify({"msg": "User is not registered"}), 401
    
    if user.is_admin is False:
        return jsonify({"msg": "Access forbidden"}), 403

    if password != user.password :
        return jsonify({"msg": "Wrong password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
   
    if user is None:
        return jsonify({"msg": "User is not registered"}), 401

    if password != user.password :
        return jsonify({"msg": "Wrong password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route("/signup", methods=["POST"])
def signup():
    body = request.get_json()
    user = User.query.filter_by(email=body["email"]).first()

    if user == None:
        user = User(name=body["name"], email=body["email"], password=body["password"], is_active=True, is_admin=False)

        db.session.add(user)
        db.session.commit()
        user_info = user.serialize()
        access_token = create_access_token(identity=user_info["id"])
        user_info['access_token']=access_token

        return jsonify(user_info), 200
    else:
        return jsonify({"msg": "user already exists with this email address"}), 401

@api.route("/admin_signup", methods=["POST"])
def admin_signup():
    body = request.get_json()
    user = User.query.filter_by(email=body["email"]).first()

    if user == None:
        user = User(name=body["name"], email=body["email"], password=body["password"], is_active=True, is_admin=True)

        db.session.add(user)
        db.session.commit()
        user_info = user.serialize()
        access_token = create_access_token(identity=user_info["id"])
        user_info['access_token']=access_token

        return jsonify(user_info), 200
    else:
        return jsonify({"msg": "user already exists with this email address"}), 401
    
@api.route('/get_addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    user_info = user.serialize()
    all_addresses = UserAddress.query.filter_by(user_id=user_info["id"]).all()
    result = list(map(lambda item: item.serialize(), all_addresses))

    return jsonify(result) 

@api.route('/add_address', methods=['POST'])
@jwt_required()
def add_address():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    user_info = user.serialize()
    current_user_id = user_info["id"]

    body = request.get_json()

    address = Address(
        name = body['name'],
        directions = body['directions'],
        district = body['district'],
        province = body['province'],
        state = body['state']
    )
    db.session.add(address)
    db.session.commit()

    address_created = Address.query.filter_by(directions=body['directions']).first()
    address_created_info = address_created.serialize()
    user_address = UserAddress(
        user_id = current_user_id,
        address_id = address_created_info["id"],
        is_default = body['is_default']
    )
    db.session.add(user_address)
    db.session.commit()

    response_body = {
        "message": "Address created"
    }

    return jsonify(response_body), 200

@api.route('/update_address/<int:address_id>', methods =['PUT'])
@jwt_required()
def update_address(address_id):
    body = request.get_json()
    update_address = Address.query.filter_by(id=address_id).first()
    print(update_address)
    print(body)
    if body['name']: update_address.name = body['name']
    if body['directions']: update_address.directions = body['directions']
    if body['district']: update_address.district = body['district']
    if body['province']: update_address.province = body['province']
    if body['state']: update_address.state = body['state']

    db.session.commit()

    response_body = {
        "message": "Address updated"
    }
      
    return jsonify(response_body), 200


@api.route('/delete_address/<int:address_id>', methods =['DELETE'])
def delete_address(address_id):
    delete_address = Address.query.filter_by(id=address_id).first()

    db.session.delete(delete_address)
    db.session.commit()

    response_body = {
        "message": "Address deleted"
    }
      
    return jsonify(response_body), 200

@api.route('/get_products', methods=['GET'])
def get_products():
    
    all_products = ProductItem.query.all()
    result = list(map(lambda item: item.serialize(), all_products))

    return jsonify(result) 

@api.route('/add_products', methods=['POST'])
@jwt_required()
def add_products():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()

    if user.is_admin is True:

        product = Products(
        name = body['name'],
        description = body['description'],
        )
        db.session.add(product)
        db.session.commit()

    response_body = {
        "message": "Product created"
    }

    return jsonify(response_body), 200

@api.route('/add_variation', methods=['POST'])
@jwt_required()
def add_variation():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()

    if user.is_admin is True:

        variation = Variation(
        name = body['name']
        )
        db.session.add(variation)
        db.session.commit()

    response_body = {
        "message": "Variation created"
    }

    return jsonify(response_body), 200

@api.route('/add_variation_option/<int:variation_id>', methods=['POST'])
@jwt_required()
def add_variation_option(variation_id):
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()

    if user.is_admin is True:

        variation_option = VariationOption(
        value = body['value'],
        variation_id = variation_id
        )
        db.session.add(variation_option)
        db.session.commit()

    response_body = {
        "message": "Variation created"
    }

    return jsonify(response_body), 200

@api.route('/add_product_item/<int:product_id>', methods=['POST'])
@jwt_required()
def add_product_item(product_id):
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()

    if user.is_admin is True:

        product_item = ProductItem(
        product_id = product_id,
        sku = body['sku'],
        qty_in_stock = body['qty_in_stock'],
        #product_image check how to add image
        price = body['price']
        )
        db.session.add(product_item)
        db.session.commit()

    response_body = {
        "message": "Product item created"
    }

    return jsonify(response_body), 200


