  
import os
from flask_admin import Admin
from api.models import db, User, Address, UserAddress, ProductCategory, Promotion, PromotionCategory, Products, ProductItem
from api.models import Size, Material, Crystal, PaymentType, ShoppingCart, ShoppingCartItem
from api.models import ShippingMethod, ShopOrder, OrderLine, UserReview
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Permanus Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Address, db.session))
    admin.add_view(ModelView(UserAddress, db.session))
    admin.add_view(ModelView(ProductCategory, db.session))
    admin.add_view(ModelView(Promotion, db.session))
    admin.add_view(ModelView(PromotionCategory, db.session))
    admin.add_view(ModelView(Products, db.session))
    admin.add_view(ModelView(ProductItem, db.session))
    admin.add_view(ModelView(Size, db.session))
    admin.add_view(ModelView(Material, db.session))
    admin.add_view(ModelView(Crystal, db.session))
    admin.add_view(ModelView(PaymentType, db.session))
    admin.add_view(ModelView(ShoppingCart, db.session))
    admin.add_view(ModelView(ShoppingCartItem, db.session))
    admin.add_view(ModelView(ShippingMethod, db.session))
    admin.add_view(ModelView(ShopOrder, db.session))
    admin.add_view(ModelView(OrderLine, db.session))
    admin.add_view(ModelView(UserReview, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))