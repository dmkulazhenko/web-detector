from typing import Dict, Tuple
from uuid import uuid4

from celery.result import AsyncResult
from flask import current_app
from werkzeug.datastructures import FileStorage

from web import celery
from web.utils import message


class DetectorDetectService:
    @staticmethod
    def save_video(video: FileStorage) -> str:
        """Saves video to storage and returns video id.

        :param video: FileStorage video object
        :returns: id of saved video
        """
        video_id = uuid4().hex
        video.save(current_app.config["VIDEO_STORAGE"] / video_id)
        return video_id

    @staticmethod
    def create_new_job(video_id: str) -> Tuple[Dict, int]:
        """Creates new celery job for processing and returns http response.

        :param video_id: id of video in storage
        :returns: HTTP response object (dict) and http return code
        """
        task = celery.send_task(
            "detector.processor.process_video",
            args=(video_id,),
            queue="processor",
        )

        resp = message(True, "Job successfully created.")
        resp["job_id"] = task.id
        return resp, 201


class DetectorResultsService:
    @staticmethod
    def _generate_empty_response() -> Dict:
        resp = message(
            False, "Processor task is in queue or job_id is invalid"
        )
        resp.update(
            {
                "processor_task": {
                    "id": None,
                    "state": None,
                },
                "detector_chord": {
                    "id": None,
                    "state": None,
                },
                "result": None,
            }
        )
        return resp

    @staticmethod
    def _fill_processor_task_info(
        resp: Dict, processor_task: AsyncResult
    ) -> int:
        resp["processor_task"]["id"] = processor_task.id
        resp["processor_task"]["state"] = processor_task.state
        return_code = 221

        if processor_task.successful():
            resp["message"] = "Processor task completed successfully"
        elif processor_task.state == "STARTED":
            resp["message"] = "Processor task is in progress"
        elif processor_task.failed():
            resp["message"] = "Processor task failed"
            return_code = 551
        else:
            resp["message"] = "Processor task is in queue or job_id is invalid"

        return return_code

    @staticmethod
    def _fill_detector_chord_info(
        resp: Dict, detector_chord: AsyncResult
    ) -> int:
        resp["detector_chord"]["id"] = detector_chord.id
        resp["detector_chord"]["state"] = detector_chord.state
        return_code = 221

        if detector_chord.successful():
            # Maybe overwritten later as far as whole job completed
            resp["message"] = "Detector chord completed successfully"
        elif detector_chord.state == "STARTED":
            resp["message"] = "Detector chord is on final stage"
        elif detector_chord.failed():
            resp["message"] = "Detector chord failed"
            return_code = 552
        else:
            resp["message"] = "Detector chord is in queue or in progress"

        return return_code

    @classmethod
    def parse_jobs_results(cls, job_id: str) -> Tuple[Dict, int]:
        """Checks celery tasks statuses and returns http response.

        HTTP Codes:
        200 - Job completed & results available
        221 - Job in progress / queue
        551 - Job failed (processor task failed)
        552 - Job failed (detector chord failed)

        :param job_id: Job id (namely job id == processor task id)
        :returns: HTTP response object (dict) and http return code
        """
        resp = cls._generate_empty_response()

        processor_task: AsyncResult = celery.AsyncResult(job_id)
        return_code = cls._fill_processor_task_info(resp, processor_task)

        if not processor_task.successful():
            return resp, return_code

        # Processor generated chord and we can parse info about it
        detector_chord_id = processor_task.get()
        detector_chord: AsyncResult = celery.AsyncResult(detector_chord_id)
        return_code = cls._fill_detector_chord_info(resp, detector_chord)

        if not detector_chord.successful():
            return resp, return_code

        # Chord finished, so job completed
        resp["status"] = True
        resp["message"] = "Job completed successfully"
        resp["result"] = detector_chord.get()
        return resp, 200
