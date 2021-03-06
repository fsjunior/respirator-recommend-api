from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine

from app.api.routes import configure_routes
from app.cache import configure_cache
from app.config import FlaskConfiguration


def create_app():
    app = Flask("respirator-recommend-api")
    app.config.from_object(FlaskConfiguration)

    configure_cors(app)
    configure_marshmallow(app)
    configure_routes(app)
    configure_cache(app)
    configure_mongodb(app)

    return app


def configure_cors(app):
    CORS(app, resources={r"/*": {"origins": "https://respirator-recommend-api.chico.codes", "send_wildcard": "False"}})


def configure_marshmallow(app: Flask):
    Marshmallow(app)


def configure_mongodb(app: Flask):
    MongoEngine(app)
