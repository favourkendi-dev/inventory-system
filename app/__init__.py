from flask import Flask
from app.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import inventory_bp
    app.register_blueprint(inventory_bp)

    return app