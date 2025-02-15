import logging
import sys
from logging.config import dictConfig

from app.core.config import settings


def configure_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s | %(asctime)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "fmt": "%(asctime)s %(levelname)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "simon.log",
                "formatter": "json",
                "encoding": "utf8",
            },
        },
        "loggers": {
            "simon": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "propagate": False,
            }
        },
    }

    dictConfig(log_config)
    return logging.getLogger("simon")


logger = configure_logging()
