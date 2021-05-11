from flask_restx import Resource
from flask_jwt_extended import jwt_required

from web.utils import message

from .dto import DetectorDto
from .upload_dto import gen_detect_upload_request

api = DetectorDto.api
detect_upload_request = gen_detect_upload_request()


@api.route("/detect")
class DetectorDetect(Resource):
    @api.doc(
        "Detect objects",
        responses={
            201: ("Job created.", DetectorDto.detect_success),
            400: "Validations failed.",
        }
    )
    @api.expect(detect_upload_request)
    # @jwt_required()
    def post(self):
        video = detect_upload_request.parse_args()["video"]
        video.read()
        return message(True, "Hello"), 201


@api.route("/results/<string:job_id>")
class DetectorResults(Resource):
    # @jwt_required()
    @api.doc(
        "Detect results",
        responses={
            200: ("Job id found.", DetectorDto.detect_results),
            404: "Job with such id not found.",
        }
    )
    @api.expect(DetectorDto.detect_results)
    def get(self, job_id):
        return message(True, job_id)
