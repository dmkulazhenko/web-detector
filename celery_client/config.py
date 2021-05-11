import os
from typing import Type


class Config:
    CELERY_BROKER = os.environ.get("CELERY_BROKER_URL")
    CELERY_BACKEND = os.environ.get("CELERY_BROKER_URL")

    task_serializer = "json"
    accept_content = ["json"]
    result_serializer = "json"
    timezone = "Europe/Minsk"
    enable_utc = True


class ProcessorConfig(Config):
    imports = ["detector.processor"]


class DetectorConfig(Config):
    imports = ["detector.detector"]


class ClientConfig(Config):
    pass


_config_map = {
    "PROCESSOR": ProcessorConfig,
    "DETECTOR": DetectorConfig,
    "CLIENT": ClientConfig,
}


def get_config_by_name(config_name: str = "CLIENT") -> Type[Config]:
    return _config_map[config_name or "CLIENT"]
