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
    from milkanalyzer.aimodels.routes import aimodels
    from milkanalyzer.values.routes import values
    from milkanalyzer.errors.error_handlers import errors
    from milkanalyzer.predictions.routes import predictions

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(aimodels)
    app.register_blueprint(values)
    app.register_blueprint(errors)
    app.register_blueprint(predictions)

    return app

def new_api(app):
    api=Api(app, doc='/api', title="Milk Analyzer API", description="REST API for the Milk Analyzer service")
    return api

with new_app().app_context():
    db.create_all()

