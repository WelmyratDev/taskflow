import logging
import logging.config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "taskflow": {
            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)-30s | "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "taskflow",
            "stream": "ext://sys.stdout",
        },

        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "taskflow",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },

    "loggers": {
        "taskflow": {
            "handlers": [
                "console",
                "file",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },

    "root": {
        "handlers": [],
        "level": "WARNING",
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)