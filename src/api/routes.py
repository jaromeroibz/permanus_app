"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, Response
from api.models import db, User, Address, UserAddress, ProductCategory, Promotion, PromotionCategory, Products, ProductItem
from api.models import Size, Crystal, Material, PaymentType, UserPaymentMethod, ShoppingCart, ShoppingCartItem
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

@api.route('/get_all_products', methods=['GET'])
def get_all_products():
    
    all_products = Products.query.all()
    result = list(map(lambda item: item.serialize(), all_products))

    return jsonify(result) 

@api.route('/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    
    product = Products.query.filter_by(id=product_id).first()

    return jsonify(product.serialize())

@api.route('/add_products', methods=['POST'])
@jwt_required()
def add_products():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()
    product = Products.query.filter_by(name=body["name"]).first()
    category = ProductCategory.query.filter_by(category_name=body["category_name"]).first()
    category_info = category.serialize()

    if user.is_admin is True and product == None:

        product = Products(
        name = body['name'],
        description = body['description'],
        category_id = category_info['id']
        )
        db.session.add(product)
        db.session.commit()

        response_body = {
            "message": "Product created"
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "product already exists with this name"}), 401

@api.route('/update_products/<int:product_id>', methods =['PUT'])
@jwt_required()
def update_products(product_id):
    body = request.get_json()
    update_product = Products.query.filter_by(id=product_id).first()
    category = ProductCategory.query.filter_by(category_name=body["category_name"]).first()
    category_info = category.serialize()
   
    if body['name']: update_product.name = body['name']
    if body['description']: update_product.description = body['description']
    if body['category_name']: update_product.category_id = category_info['id']

    db.session.commit()

    response_body = {
        "message": "Product updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_product/<int:product_id>', methods =['DELETE'])
def delete_product(product_id):
    delete_product = Products.query.filter_by(id=product_id).first()

    db.session.delete(delete_product)
    db.session.commit()

    response_body = {
        "message": "Product deleted"
    }
      
    return jsonify(response_body), 200

# Variation Services

@api.route('/get_size', methods=['GET'])
def get_size():
    
    all_sizes= Size.query.all()
    result = list(map(lambda item: item.serialize(), all_sizes))

    return jsonify(result) 

@api.route('/add_size', methods=['POST'])
@jwt_required()
def add_size():
    
    current_user = get_jwt_identity()
    body = request.get_json()
    user = User.query.filter_by(email=current_user).first()
    size = Size.query.filter_by(size_value=body['size_value']).first()

    if user.is_admin is True and size == None:

        size = Size(
        size_value = body['size_value'])
        db.session.add(size)
        db.session.commit()

    response_body = {
        "message": "Size value created"
    }

    return jsonify(response_body), 200

@api.route('/update_size/<int:size_id>', methods =['PUT'])
@jwt_required()
def update_size(size_id):
    body = request.get_json()
    update_size = Size.query.filter_by(id=size_id).first()
    
    if body['size_value']: update_size.size_value = body['size_value']

    db.session.commit()

    response_body = {
        "message": "Size value updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_size/<int:size_id>', methods =['DELETE'])
def delete_size(size_id):
    delete_size = Size.query.filter_by(id=size_id).first()
    # all_product_item = ProductItem.query.filter_by(size_id=size_id).all()
    # result = list(map(lambda item: item.serialize(), all_product_item))
    # print(result)

    db.session.delete(delete_size)
    db.session.commit()

    response_body = {
        "message": "Size deleted"
    }
      
    return jsonify(response_body), 200

@api.route('/get_material', methods=['GET'])
def get_material():
    
    all_materials= Material.query.all()
    result = list(map(lambda item: item.serialize(), all_materials))

    return jsonify(result) 

@api.route('/add_material', methods=['POST'])
@jwt_required()
def add_material():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()
    material = Material.query.filter_by(material_value=body['material_value']).first()

    if user.is_admin is True and material == None:

        material = Material(
        material_value = body['material_value'])
        db.session.add(material)
        db.session.commit()

    response_body = {
        "message": "Material value created"
    }

    return jsonify(response_body), 200

@api.route('/update_material/<int:material_id>', methods =['PUT'])
@jwt_required()
def update_material(material_id):
    body = request.get_json()
    update_material = Material.query.filter_by(id=material_id).first()
    
    if body['material_value']: update_material.material_value = body['material_value']

    db.session.commit()

    response_body = {
        "message": "Material value updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_material/<int:material_id>', methods =['DELETE'])
def delete_material(material_id):
    delete_material = Material.query.filter_by(id=material_id).first()

    db.session.delete(delete_material)
    db.session.commit()

    response_body = {
        "message": "Material deleted"
    }
      
    return jsonify(response_body), 200

@api.route('/get_crystal', methods=['GET'])
def get_crystal():
    
    all_crystals= Crystal.query.all()
    result = list(map(lambda item: item.serialize(), all_crystals))

    return jsonify(result) 

@api.route('/add_crystal', methods=['POST'])
@jwt_required()
def add_crystal():
    
    current_user = get_jwt_identity()
    body = request.get_json()
    user = User.query.filter_by(email=current_user).first()
    crystal = Crystal.query.filter_by(crystal_value=body['crystal_value']).first()

    if user.is_admin is True and crystal == None:

        crystal = Crystal(
        crystal_value = body['crystal_value'])
        db.session.add(crystal)
        db.session.commit()

    response_body = {
        "message": "Crystal value created"
    }

    return jsonify(response_body), 200

@api.route('/update_crystal/<int:crystal_id>', methods =['PUT'])
@jwt_required()
def update_crystal(crystal_id):
    body = request.get_json()
    update_crystal = Crystal.query.filter_by(id=crystal_id).first()
    
    if body['crystal_value']: update_crystal.crystal_value = body['crystal_value']

    db.session.commit()

    response_body = {
        "message": "Crystal value updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_crystal/<int:crystal_id>', methods =['DELETE'])
def delete_crystal(crystal_id):
    delete_crystal = Crystal.query.filter_by(id=crystal_id).first()

    db.session.delete(delete_crystal)
    db.session.commit()

    response_body = {
        "message": "Crystal deleted"
    }
      
    return jsonify(response_body), 200

# Product Item services

@api.route('/get_all_product_items/<int:product_id>', methods=['GET'])
def get_all_product_items(product_id):
    
    all_product_items= ProductItem.query.filter_by(product_id=product_id).all()
    result = list(map(lambda item: item.serialize(), all_product_items))

    return jsonify(result)

@api.route('/get_product_item/<int:product_id>', methods=['GET'])
def get_product_item(product_id):
    
    body = request.get_json()
    product_item= ProductItem.query.filter_by(product_id=product_id, size_id=body['size_id'], material_id=body['material_id'], crystal_id=body['crystal_id']).first()

    return jsonify(product_item.serialize()) 

@api.route('/add_product_item/<int:product_id>', methods=['POST'])
@jwt_required()
def add_product_item(product_id):
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()
    product_item = ProductItem.query.filter_by(name=body['name']).first()
    size = Size.query.filter_by(size_value=body['size_value']).first()
    size_info = size.serialize()
    print(size_info)
    material = Material.query.filter_by(material_value=body['material_value']).first()
    material_info = material.serialize()
    crystal = Crystal.query.filter_by(crystal_value=body['crystal_value']).first()
    crystal_info = crystal.serialize()
    
    if user.is_admin is True and product_item == None:

        product_item = ProductItem(
        name = body['name'],
        product_id = product_id,
        size_id = size_info['id'],
        material_id = material_info['id'],
        crystal_id = crystal_info['id'],
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

@api.route('/update_product_item/<int:product_item_id>', methods =['PUT'])
@jwt_required()
def update_product_item(product_item_id):
    body = request.get_json()
    update_product_item = ProductItem.query.filter_by(id=product_item_id).first()
    product = Products.query.filter_by(name=body["product_name"]).first()
    product_info = product.serialize()
   
    if body['name']: update_product_item.name = body['name']
    if body['product_id']: update_product_item.product_id = product_info['id']
    if body['sku']: update_product_item.sku = body['sku']
    if body['qty_in_stock']: update_product_item.qty_in_stock = body['qty_in_stock']
    if body['price']: update_product_item.price = body['price']


    db.session.commit()

    response_body = {
        "message": "Product item updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_product_item/<int:product_item_id>', methods =['DELETE'])
def delete_product_item(product_item_id):
    delete_product_item = ProductItem.query.filter_by(id=product_item_id).first()

    db.session.delete(delete_product_item)
    db.session.commit()

    response_body = {
        "message": "Product item deleted"
    }
      
    return jsonify(response_body), 200

# Product category services

@api.route('/get_category', methods=['GET'])
def get_category():
    
    all_categories = ProductCategory.query.all()
    result = list(map(lambda item: item.serialize(), all_categories))

    return jsonify(result) 

@api.route('/add_category', methods=['POST'])
@jwt_required()
def add_category():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()
    category = ProductCategory.query.filter_by(category_name=body["category_name"]).first()

    if user.is_admin is True and category == None:

        category = ProductCategory(category_name = body['category_name'])
        db.session.add(category)
        db.session.commit()

        response_body = {
            "message": "Category created"
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Category already exists with this name"}), 401

@api.route('/update_category/<int:category_id>', methods =['PUT'])
@jwt_required()
def update_category(category_id):
    body = request.get_json()
    update_category = ProductCategory.query.filter_by(id=category_id).first()
    print(update_category)
    print(body)
    if body['category_name']: update_category.category_name = body['category_name']

    db.session.commit()

    response_body = {
        "message": "Category updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_category/<int:category_id>', methods =['DELETE'])
def delete_category(category_id):
    delete_category = ProductCategory.query.filter_by(id=category_id).first()

    db.session.delete(delete_category)
    db.session.commit()

    response_body = {
        "message": "Product category deleted"
    }
      
    return jsonify(response_body), 200

# Promotions Services

@api.route('/get_promotion', methods=['GET'])
def get_promotion():
    
    all_promotions = Promotion.query.all()
    result = list(map(lambda item: item.serialize(), all_promotions))

    return jsonify(result) 

@api.route('/add_promotion', methods=['POST'])
@jwt_required()
def add_promotion():
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    body = request.get_json()
    promotion = Promotion.query.filter_by(name=body["name"]).first()
    category = ProductCategory.query.filter_by(category_name=body["category_name"]).first()
    category_info = category.serialize()

    if user.is_admin is True and promotion == None:

        promotion = Promotion(
            name = body['name'],
            description = body['description'],
            discount_rate = body['discount_rate'],
            start_date = body['start_date'],
            end_date = body['end_date']
            )
        db.session.add(promotion)
        db.session.commit()

        promotion_info = promotion.serialize()
        promotion_category = PromotionCategory(
            category_id = category_info['id'],
            promotion_id = promotion_info['id']
        )
        db.session.add(promotion_category)
        db.session.commit()

        response_body = {
            "message": "Promotion created"
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Promotion already exists with this name"}), 401

@api.route('/update_promotion/<int:promotion_id>', methods =['PUT'])
@jwt_required()
def update_promotion(promotion_id):
    body = request.get_json()
    update_promotion = Promotion.query.filter_by(id=promotion_id).first()
    update_promotion_category = PromotionCategory.query.filter_by(promotion_id=promotion_id).first()
    category = ProductCategory.query.filter_by(category_name=body["category_name"]).first()
    category_info = category.serialize()

    if body['name']: update_promotion.name = body['name']
    if body['description']: update_promotion.description = body['description']
    if body['discount_rate']: update_promotion.discount_rate = body['discount_rate']
    if body['start_date']: update_promotion.start_date = body['start_date']
    if body['end_date']: update_promotion.end_date = body['end_date']
    if body['category_name']: update_promotion_category.category_id = category_info['id']


    db.session.commit()

    response_body = {
        "message": "Promotion updated"
    }
      
    return jsonify(response_body), 200

@api.route('/delete_promotion/<int:promotion_id>', methods =['DELETE'])
def delete_promotion(promotion_id):
    delete_promotion = Promotion.query.filter_by(id=promotion_id).first()

    db.session.delete(delete_promotion)
    db.session.commit()

    response_body = {
        "message": "Promotion deleted"
    }
      
    return jsonify(response_body), 200

