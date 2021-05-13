"""
Extensions module

Each extension is initialized when app is created.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

bcrypt = Bcrypt()
migrate = Migrate()

jwt = JWTManager()
ma = Marshmallow()
