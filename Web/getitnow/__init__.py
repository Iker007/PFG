from flask import Flask
from getitnow.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_view = 'users.login'

mail = Mail()

bcrypt = Bcrypt()

def new_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from getitnow.main.routes import main
    from getitnow.users.routes import users
    from getitnow.restaurants.routes import restaurants
    from getitnow.products.routes import products
    from getitnow.orders.routes import orders
    from getitnow.payment.routes import payment
    from getitnow.errors.error_handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(restaurants)
    app.register_blueprint(products)
    app.register_blueprint(orders)
    app.register_blueprint(payment)
    app.register_blueprint(errors)

    return app

def new_api(app):
    api=Api(app, doc='/api', title="Get It Now API", description="REST API for Get It Now")
    return api

with new_app().app_context():
    db.create_all()

