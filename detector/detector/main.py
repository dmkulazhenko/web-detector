from threading import local

from detectron2.config import get_cfg

from .config import DETECTRON_MODEL_CFG, DETECTRON_MODEL_TS
from .detector_celery import celery
from .predictor import Predictor

local_storage = local()


def get_model_cfg():
    # Mount volume with torch models to cache models
    cfg = get_cfg()
    cfg.merge_from_file(DETECTRON_MODEL_CFG)
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = DETECTRON_MODEL_TS
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = DETECTRON_MODEL_TS
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = (
        DETECTRON_MODEL_TS
    )
    cfg.freeze()
    return cfg


def get_predictor() -> Predictor:
    # cache predictor object, as far as initialization is pretty expensive
    if not hasattr(local_storage, "predictor"):
        local_storage.predictor = Predictor(get_model_cfg())
    return local_storage.predictor


@celery.task(name="detector.detector.detect_frames")
def detect_frames(frames):
    predictor = get_predictor()
    predictions = predictor.run_on_frames(frames)

    labels = list(predictor.metadata.thing_classes)
    result = []
    for prediction in predictions:
        result.append(
            [
                (labels[int(cls_)], float(scr))
                for cls_, scr in zip(
                    prediction["instances"].get("pred_classes"),
                    prediction["instances"].get("scores"),
                )
            ]
        )
    return result
