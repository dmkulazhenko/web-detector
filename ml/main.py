import multiprocessing as mp

import cv2
from config import DETECTRON_MODEL_CFG, DETECTRON_MODEL_TS
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from predictor import Predictor


def get_model_cfg():
    cfg = get_cfg()
    cfg.merge_from_file(DETECTRON_MODEL_CFG)
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = DETECTRON_MODEL_TS
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = DETECTRON_MODEL_TS
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = (
        DETECTRON_MODEL_TS
    )
    cfg.freeze()
    return cfg


def image(model, img_path):
    img = read_image(img_path, format="BGR")

    predictions = model.run_on_image(img)
    labels = list(model.metadata.thing_classes)

    return [
        (labels[int(cls_)], float(scr))
        for cls_, scr in zip(
            predictions["instances"].get("pred_classes"),
            predictions["instances"].get("scores"),
        )
    ]


def video(model, vid_path):
    vid = cv2.VideoCapture(vid_path)

    predictions = model.run_on_video(vid)
    labels = list(model.metadata.thing_classes)

    for prediction in predictions:
        yield [
            (labels[int(cls_)], float(scr))
            for cls_, scr in zip(
                prediction["instances"].get("pred_classes"),
                prediction["instances"].get("scores"),
            )
        ]

    vid.release()


def main():
    if mp.get_start_method(allow_none=True) != 'spawn':
        mp.set_start_method('spawn', force=True)

    cfg = get_model_cfg()
    model = Predictor(cfg)

    if input("Type: ") == "img":
        print(image(model, input("Path to image: ")))
    else:
        res = [i for i in video(model, input("Path to video: "))]
        print("Total frames: ", len(res))
        print(res)


if __name__ == "__main__":
    main()
