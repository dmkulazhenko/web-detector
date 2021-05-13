from flask import Blueprint
from flask_restx import Api

from .detector.controller import api as detector_ns

api_bp = Blueprint("api", __name__, url_prefix="/api")

authorizations = {
    "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    api_bp,
    title="DetectronAPI",
    description="Detect objects using Detectron2",
    authorizations=authorizations,
    security="api_key",
)

api.add_namespace(detector_ns)
