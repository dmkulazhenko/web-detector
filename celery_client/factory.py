from celery import Celery

from .config import get_config_by_name


def create_celery(config_name: str) -> Celery:
    config = get_config_by_name(config_name)
    return Celery(
        main="detector",
        broker=config.CELERY_BROKER,
        backend=config.CELERY_BACKEND,
        config_source=config,
    )
