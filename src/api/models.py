from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from enum import Enum

db = SQLAlchemy()
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False)   
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Address(db.Model):
    __tablename__='address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120), unique=False, nullable=False)
    directions = db.Column(db.String(120), unique=False, nullable=False)
    district = db.Column(db.String(120), unique=False, nullable=False)
    province = db.Column(db.String(120), unique=False, nullable=False)
    state = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<Address {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "directions": self.directions,
            "district": self.district,
            "province": self.province,
            "state": self.state     
        }
    
class UserAddress(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    is_default = db.Column(db.Boolean(), unique=False, nullable=False)
    user = db.relationship(User)
    address = db.relationship(Address)

    def __repr__(self):
        return f'<UserAddress {self.id}>' 
    
    def serialize(self):
        return{
            "user_id": self.user_id,
            "address_id": self.address_id,
            "is_default": self.is_default
        }
    
class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(80))    

    def __repr__(self):
        return f'<ProductCategory {self.id}>' 
    
    def serialize(self):
        return{
            "id": self.id,
            "category_name": self.category_name
        }

class Promotion(db.Model):
    __tablename__ = 'promotion'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    discount_rate = db.Column(db.Integer, unique=False, nullable=True)
    start_date = db.Column(db.String(20), unique=False, nullable=False)
    end_date = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f'<Promotion {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "discount_rate": self.discount_rate,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

class PromotionCategory(db.Model):
    __tablename__='promotion_category'
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id', ondelete="CASCADE"))
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id', ondelete="CASCADE"))
    category = db.relationship(ProductCategory)
    promotion = db.relationship(Promotion)

    def __repr__(self):
        return f'<PromotionCategory {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "category_id": self.category_id,
            "promotion_id": self.promotion_id
        }

class Size(db.Model):
    __tablename__ = 'size'
    id = db.Column(db.Integer, primary_key = True)
    size_value = db.Column(db.String(10), nullable = False, unique = True)
    product_item = db.relationship("ProductItem", cascade = "all, delete, delete-orphan", passive_deletes=True, back_populates="size")

    def __repr__(self):
        return f'<Size {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "size_value": self.size_value
        }

class Crystal(db.Model):
    __tablename__ = 'crystal'
    id = db.Column(db.Integer, primary_key = True)
    crystal_value = db.Column(db.String(10), nullable = False, unique = True)
    product_item = db.relationship("ProductItem", cascade = "all, delete, delete-orphan", passive_deletes=True, back_populates="crystal")

    def __repr__(self):
        return f'<Crystal {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "crystal_value": self.crystal_value
        }

class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key = True)
    material_value = db.Column(db.String(10), nullable = False, unique = True)
    product_item = db.relationship("ProductItem", cascade = "all, delete, delete-orphan", passive_deletes=True, back_populates="material")

    def __repr__(self):
        return f'<Material {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "material_value": self.material_value
        }

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id', ondelete="CASCADE"))
    category = db.relationship("ProductCategory")
    product_item = db.relationship("ProductItem", cascade = "all, delete, delete-orphan", passive_deletes=True, back_populates="products")
    #product_image figure out how to add image    


    def __repr__(self):
        return f'<Products {self.id}>' 
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }    
    
class ProductItem(db.Model):
    __tablename__ = 'product_item'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"))
    size_id = db.Column(db.Integer, db.ForeignKey('size.id', ondelete="CASCADE"))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id', ondelete="CASCADE"))
    crystal_id = db.Column(db.Integer, db.ForeignKey('crystal.id', ondelete="CASCADE"))
    products = db.relationship(Products, back_populates="product_item")
    size = db.relationship(Size, back_populates="product_item")
    material = db.relationship(Material, back_populates="product_item")
    crystal = db.relationship(Crystal, back_populates="product_item")
    sku = db.Column(db.Integer, nullable = False, unique = True)
    qty_in_stock = db.Column(db.Integer, nullable = False, unique = False)
    price = db.Column(db.Integer, nullable = False, unique = False)
    #product_image figure out how to add image
    product_image = db.Column(db.String(300), nullable = True, unique = True)    

    def __repr__(self):
        return f'<ProductItem {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "product_id": self.product_id,
            "size_id": self.size_id,
            "material_id": self.material_id,
            "crystal_id": self.crystal_id,
            "sku": self.sku,
            "qty_in_stock": self.qty_in_stock,
            "price": self.price,
            "product_image": self.product_image
        }  
    
class PaymentType(db.Model):
    __tablename__ = 'payment_type'
    id = db.Column(db.Integer, primary_key = True)
    payment_type = db.Column(db.String(80), nullable = False, unique = True)

    def __repr__(self):
        return f'<PaymentType {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "payment_type": self.payment_type
        }

class UserPaymentMethod(db.Model):
    __tablename__ = 'user_payment_method'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))
    provider = db.Column(db.String(80), nullable = False, unique = False)
    account_number = db.Column(db.String(80), nullable = False, unique = False)
    expiry_date = db.Column(db.String(5), nullable = False, unique = False)
    is_default = db.Column(db.Boolean(), unique=False, nullable=False)
    payment_type = db.relationship(PaymentType)
    user = db.relationship(User)

    def __repr__(self):
        return f'<UserPaymentMethod {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "payment_type_id": self.payment_type_id,
            "provider": self.provider,
            "account_number": self.account_number,
            "expiry_date":self.expiry_date,
            "is_default": self.is_default
        }
    
class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    def __repr__(self):
        return f'<ShoppingCart {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.id
        }

class ShoppingCartItem(db.Model):
    __tablename__ = 'shopping_cart_item'
    id = db.Column(db.Integer, primary_key = True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'))
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'))
    qty = db.Column(db.Integer, nullable = False, unique = False)

    def __repr__(self):
        return f'<ShoppingCartItem>'
    
    def serialize(self):
        return{
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id
        }

class OrderStatus(Enum): 

    ordered = 'ordered',
    processed = 'processed',
    delivered = 'delivered'

class ShippingMethod(db.Model):
    __tablename__ = 'shipping_method'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True)
    price = db.Column(db.Integer, nullable = False, unique = False)

    def __repr__(self):
        return f'<ShippingMethod>'
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
    
class ShopOrder(db.Model):
    __tablename__ = 'shop_order'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_payment_method_id = db.Column(db.Integer, db.ForeignKey('user_payment_method.id'))
    order_date = db.Column(db.String(80), nullable = False, unique = False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    order_total = db.Column(db.Integer, nullable = False, unique = False)
    order_status = db.Column(db.String(80), nullable = False, unique = False)
    shipping_method_id = db.Column(db.Integer, db.ForeignKey('shipping_method.id'))
    shipping_method = db.relationship(ShippingMethod)
    user_payment_method = db.relationship(UserPaymentMethod)
    user = db.relationship(User)
    shipping_address = db.relationship(Address)
    

    def __repr__(self):
        return f'<ShopOrder {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "user_payment_method_id": self.user_payment_method_id,
            "order_date": self.order_date,
            "shipping_address_id": self.shipping_address_id,
            "order_total": self.order_total,
            "order_status": self.order_status,
            "shipping_method_id": self.shipping_method_id
        }
    
class OrderLine(db.Model):
    __tablename__ = 'order_line'
    id = db.Column(db.Integer, primary_key = True)
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('shop_order.id'))
    qty = db.Column(db.Integer, nullable = False, unique = False)
    order = db.relationship(ShopOrder)
    product_item = db.relationship(ProductItem)

    def __repr__(self):
        return f'<OrderLine {self.id}>'
    
    def serialize(self):
        return {

            "id": self.id,
            "product_id": self.product_id,
            "order_id": self.order_id,
            "qty": self.qty

        }

class UserReview(db.Model):
    __tablename__ = 'user_review'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ordered_product_id = db.Column(db.ForeignKey('order_line.id'))
    user = db.relationship(User)
    ordered_product = db.relationship(OrderLine)
    rating_value = db.Column(db.Integer, nullable = False, unique=False)
    comment = db.Column(db.Text, nullable = True, unique = False )

    def __repr__(self):
        return f'<UserReview> {self.id}'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.id,
            "ordered_product_id": self.id,
            "rating_value": self.rating_value,
            "comment": self.comment
        }


class UserImg(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User)
  
    def __repr__(self):
        return f'<Img {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "img": self.img,
            "name": self.name,
            "mimetype": self.mimetype,
            "user_id": self.user_id
        }
    
class ProductImg(db.Model):
    __tablename__ = 'product_img'
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = relationship(Products)
  
    def __repr__(self):
        return f'<Img {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "img": self.img,
            "name": self.name,
            "mimetype": self.mimetype,
            "product_id": self.product_id
        }

class PaymentTypeImg(db.Model):
    __tablename__ = 'payment_type_img'
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))
    payment_type = relationship(PaymentType)
  
    def __repr__(self):
        return f'<Img {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "img": self.img,
            "name": self.name,
            "mimetype": self.mimetype,
            "payment_type_id": self.payment_type_id
        }
