from werkzeug.datastructures import FileStorage

from .dto import DetectorDto


def gen_detect_upload_request():
    parser = DetectorDto.api.parser()
    parser.add_argument(
        "video", type=FileStorage, location="files", required=True
    )
    return parser
