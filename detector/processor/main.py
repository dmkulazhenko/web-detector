from typing import Dict, List

from celery import chord, signature
from cv2 import VideoCapture

from .config import Config
from .processor_celery import celery


def _frame_from_video(video):
    while video.isOpened():
        success, frame = video.read()
        if success:
            yield frame
        else:
            break


def _chunkit(generator):
    chunk = []
    for obj in generator:
        chunk.append(obj)
        if len(chunk) >= Config.CHUNK_SIZE:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk


@celery.task(name="detector.processor.merge_chunks")
def merge_chunks(results: List[List[Dict[str, float]]]):
    result = []
    for res in results:
        result.extend(res)
    return result


@celery.task(name="detector.processor.process_video")
def process_video(video_name: str):
    video = VideoCapture(str(Config.VIDEO_STORAGE / video_name))
    frames = _frame_from_video(video)

    chord_obj = chord(
        [
            signature(
                "detector.detector.detect_frames",
                args=(chunk,),
                queue="detector",
            )
            for chunk in _chunkit(frames)
        ],
        body=signature("detector.processor.merge_chunks", queue="processor"),
    )
    chord_res = chord_obj()
    return chord_res.id
