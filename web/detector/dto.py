from flask_restx import Namespace, fields


class DetectorDto:
    api = Namespace("detector", description="Detect objects using Detectron2.")

    detect_success = api.model(
        "Detect success response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "job_id": fields.String,
        },
    )

    detect_results = api.model(
        "Detect results response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "job_state": fields.String,
            "results": fields.List
        }
    )
