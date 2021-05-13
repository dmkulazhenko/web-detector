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

    detect_task_info = api.model(
        "Task metadata",
        {
            "id": fields.String(allow_none=True),
            "state": fields.String(allow_none=True),
        },
    )

    detect_results = api.model(
        "Detect results response (with info about job)",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "processor_task": fields.Nested(detect_task_info),
            "detector_chord": fields.Nested(detect_task_info),
            "result": fields.List(
                fields.Wildcard(fields.String), allow_none=True
            ),
        },
    )
