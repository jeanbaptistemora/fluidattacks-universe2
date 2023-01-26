import boto3
import bugsnag
import importlib
from logging import (
    LogRecord,
)
import logging.config
import os
import sys


class RequireProdEnvironment(logging.Filter):
    def filter(self, _: LogRecord) -> bool:
        return os.environ["ENVIRONMENT"] == "prod"


def initialize_settings() -> None:
    bugsnag.configure(
        api_key=os.environ["BUGSNAG_API_KEY_STREAMS"],
        app_type="worker",
        app_version=os.environ["CI_COMMIT_SHA"],
        notify_release_stages=["prod"],
        project_root=os.path.dirname(os.path.abspath(__file__)),
        release_stage=os.environ["ENVIRONMENT"],
    )
    bugsnag.start_session()
    logging.config.dictConfig(
        {
            "filters": {
                "require_prod_env": {"()": RequireProdEnvironment},
            },
            "formatters": {
                "pretty": {
                    "format": (
                        "[%(levelname)s] %(asctime)s - "
                        "ID:%(request_id)s - %(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%ST%z",
                }
            },
            "handlers": {
                "bugsnag": {
                    "class": "bugsnag.handlers.BugsnagHandler",
                    "extra_fields": {"extra": ["extra"]},
                    "level": "WARNING",
                },
                "cloudwatch": {
                    "class": "watchtower.CloudWatchLogHandler",
                    "filters": ["require_prod_env"],
                    "formatter": "pretty",
                    "level": "INFO",
                    "boto3_client": boto3.client("logs"),
                    "create_log_group": False,
                    "create_log_stream": False,
                    "log_group_name": "FLUID",
                    "log_stream_name": "streams_hooks",
                },
                "console": {"class": "logging.StreamHandler", "level": "INFO"},
            },
            "loggers": {
                "": {
                    "handlers": ["bugsnag", "console"],
                    "level": "INFO",
                },
                "cloudwatch": {"handlers": ["cloudwatch"], "level": "INFO"},
            },
            "version": 1,
        }
    )


def invoke_consumer(module_name: str) -> None:
    """Invokes the requested consumer"""
    consumer = importlib.import_module(f"{module_name}.consumer")
    consumer.consume()


if __name__ == "__main__":
    initialize_settings()
    invoke_consumer(sys.argv[1])
