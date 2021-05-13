from flask_jwt_extended import jwt_required
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from .dto import DetectorDto
from .service import DetectorDetectService, DetectorResultsService
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
        },
        security="api_key",
    )
    @api.expect(detect_upload_request)
    @jwt_required()
    def post(self):
        video: FileStorage = detect_upload_request.parse_args()["video"]
        video_id = DetectorDetectService.save_video(video)

        return DetectorDetectService.create_new_job(video_id)


# noinspection PyUnresolvedReferences
@api.route("/results/<string:job_id>")
class DetectorResults(Resource):
    @api.doc(
        "Detect results",
        responses={
            200: ("Job completed successfully.", DetectorDto.detect_results),
            221: ("Job is in progress", DetectorDto.detect_results),
            551: (
                "Job failed (processor task failed)",
                DetectorDto.detect_results,
            ),
            552: (
                "Job failed (detector chord failed)",
                DetectorDto.detect_results,
            ),
        },
        security="api_key",
    )
    @jwt_required()
    def get(self, job_id):
        return DetectorResultsService.parse_jobs_results(job_id)
