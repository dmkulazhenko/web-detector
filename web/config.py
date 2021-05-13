import os
from datetime import timedelta
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Change the secret key in production run.
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_ME!!!")
    DEBUG = False

    # JWT Extended config
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "CHANGE_ME!!!")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # Detector config
    VIDEO_STORAGE = Path(
        os.getenv("VIDEO_STORAGE", "/home/dmitry/storage")
    ).absolute()


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "ONLY_FOR_DEV"
    JWT_SECRET_KEY = "ONLY_FOR_DEV__JWT"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "ONLY_FOR_TESTING"
    JWT_SECRET_KEY = "ONLY_FOR_TESTING__JWT"
    # In-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data.sqlite")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)
