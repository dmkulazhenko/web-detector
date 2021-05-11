from flask import Blueprint
from flask_restx import Api

from .controller import api as detectron_ns

detector_bp = Blueprint("detector", __name__)

detector = Api(
    detector_bp,
    title="Detector",
    description="Detect objects using Detectron2",
)

detector.add_namespace(detectron_ns)
