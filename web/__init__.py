""" Top level module

This module:

- Contains create_app()
- Registers extensions
"""

from flask import Flask

from .config import config_by_name
from .extensions import bcrypt, db, jwt, ma


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)

    from .auth import auth_bp

    app.register_blueprint(auth_bp)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)