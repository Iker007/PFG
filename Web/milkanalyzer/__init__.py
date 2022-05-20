from flask import Flask
from milkanalyzer.config import Config
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

    from milkanalyzer.main.routes import main
    from milkanalyzer.users.routes import users
    from milkanalyzer.restaurants.routes import restaurants
    from milkanalyzer.aimodels.routes import aimodels
    from milkanalyzer.products.routes import products
    from milkanalyzer.values.routes import values
    from milkanalyzer.orders.routes import orders
    from milkanalyzer.payment.routes import payment
    from milkanalyzer.errors.error_handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(restaurants)
    app.register_blueprint(aimodels)
    app.register_blueprint(products)
    app.register_blueprint(values)
    app.register_blueprint(orders)
    app.register_blueprint(payment)
    app.register_blueprint(errors)

    return app

def new_api(app):
    api=Api(app, doc='/api', title="Milk Analyzer API", description="REST API for the Milk Analyzer service")
    return api

with new_app().app_context():
    db.create_all()

