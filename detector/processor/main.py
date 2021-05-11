from processor_celery import celery
from celery import signature, chunks
from cv2 import VideoCapture

from .config import Config


def _frame_from_video(video):
    while video.isOpened():
        success, frame = video.read()
        if success:
            yield frame
        else:
            break

#
# def _chunkit(generator):
#     chunk = []
#     for obj in generator:
#         chunk.append(obj)
#         if len(chunk) >= Config.CHUNK_SIZE:
#             yield chunk
#         chunk.clear()
#     if len(chunk) > 0:
#         yield chunk

# @celery.task(name="detector.processor.merge_chunks")
# def merge_chunks(results: List[List[Dict[str, float]]]):
#     return [result for result in results]
#
#
# @celery.task(name="detector.processor.process_video")
# def process_video(video_name: str):
#     video = VideoCapture(str(Config / video_name))
#     frames_gen = _frame_from_video(video)
#
#     callback = signature("detector.processor.merge_chunks")
#     header = [
#         signature(
#             "detector.detector.detect_image",
#             args=(frames_chunk,)
#         )
#         for frames_chunk in _chunkit(frames_gen)
#     ]
#     return chord(header)(callback)


@celery.task(name="detector.processor.process_video")
def process_video(video_name: str):
    video = VideoCapture(str(Config.VIDEO_STORAGE / video_name))
    frames_gen = _frame_from_video(video)

    detect_image = signature("detector.detector.detect_image")
    return chunks(detect_image, frames_gen, Config.CHUNK_SIZE).group()()
