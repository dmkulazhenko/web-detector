import os
from typing import Type, Optional


class Config:
    CELERY_BROKER = os.environ.get("CELERY_BROKER_URL")
    CELERY_BACKEND = os.environ.get("CELERY_BACKEND_URL")

    task_serializer = "pickle"
    accept_content = ["pickle", "json"]
    result_serializer = "json"
    timezone = "Europe/Minsk"
    enable_utc = True
    task_create_missing_queues = True


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


def get_config_by_name(config_name: Optional[str] = "CLIENT") -> Type[Config]:
    return _config_map[config_name or "CLIENT"]
