# Settings logger-related configs


from .various import (
    BASE_DIR,
    DEBUG,
)
from boto3.session import (
    Session,
)
import bugsnag
from bugsnag_client import (
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from context import (
    CI_COMMIT_SHA,
    CI_COMMIT_SHORT_SHA,
    FI_AWS_CLOUDWATCH_ACCESS_KEY,
    FI_AWS_CLOUDWATCH_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_BUGSNAG_ACCESS_TOKEN,
    FI_ENVIRONMENT,
    LOG_LEVEL_BUGSNAG,
    LOG_LEVEL_CONSOLE,
    LOG_LEVEL_WATCHTOWER,
)
from custom_exceptions import (
    DocumentNotFound,
    UnavailabilityError,
)
from graphql import (
    GraphQLError,
)
import json
from logging import (
    LogRecord,
)
import logging.config
import os
import re
import requests  # type: ignore
from typing import (
    Any,
    Literal,
)

# logging
AWS_ACCESS_KEY_ID = FI_AWS_CLOUDWATCH_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = FI_AWS_CLOUDWATCH_SECRET_KEY  # noqa
AWS_REGION_NAME = "us-east-1"

BOTO3_SESSION = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=FI_AWS_SESSION_TOKEN,
    region_name=AWS_REGION_NAME,
)


# pylint: disable=too-few-public-methods
class RequireDebugFalse(logging.Filter):
    def filter(self, _: LogRecord) -> bool:
        return not DEBUG


class ExtraMessageFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str = "[{levelname}] {message}, extra={extra}",
        style: Literal["{"] = "{",
    ) -> None:
        logging.Formatter.__init__(self, fmt=fmt, style=style)

    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r"\{(\w+)\}")
        arg_names = [x.group(1) for x in arg_pattern.finditer(str(self._fmt))]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = None

        return super().format(record)


MODULES = os.listdir(os.path.dirname(os.path.dirname(__file__)))
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": RequireDebugFalse},
    },
    "formatters": {
        "level_message_extra": {
            "()": ExtraMessageFormatter,
        },
    },
    "handlers": {
        "bugsnag": {
            "extra_fields": {"extra": ["extra"]},
            "filters": ["require_debug_false"],
            "class": "bugsnag.handlers.BugsnagHandler",
            "level": LOG_LEVEL_BUGSNAG or "WARNING",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL_CONSOLE or "INFO",
            "formatter": "level_message_extra",
        },
        "watchtower": {
            "boto3_session": BOTO3_SESSION,
            "class": "watchtower.CloudWatchLogHandler",
            "level": LOG_LEVEL_WATCHTOWER or "INFO",
            "log_group": "FLUID",
            "filters": ["require_debug_false"],
            "stream_name": "FLUIDIntegrates",
            # Since LogGroup already exists, it was causing a
            # ThrottlingException error that resulted in 'unable to configure
            # watchtower'
            "create_log_group": False,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "transactional": {
            "handlers": ["watchtower"],
            "level": "INFO",
        },
        **{
            module: {
                "handlers": ["bugsnag"],
                "level": "WARNING",
            }
            for module in MODULES
        },
    },
}

# Force logging to load the config right away
# This is important otherwise loggers are not going to work in CI jobs
logging.config.dictConfig(LOGGING)


# bugsnag
bugsnag.configure(
    api_key=FI_BUGSNAG_ACCESS_TOKEN,
    app_version=CI_COMMIT_SHORT_SHA,
    asynchronous=True,
    auto_capture_sessions=True,
    project_root=BASE_DIR,
    release_stage=FI_ENVIRONMENT,
    send_environment=True,
)

if FI_ENVIRONMENT == "production":
    URL = "https://build.bugsnag.com"
    HEADERS = {"Content-Type": "application/json", "server": "None"}
    PAYLOAD = {
        "apiKey": FI_BUGSNAG_ACCESS_TOKEN,
        "appVersion": CI_COMMIT_SHORT_SHA,
        "releaseStage": FI_ENVIRONMENT,
        "sourceControl": {
            "provider": "gitlab",
            "repository": "https://gitlab.com/fluidattacks/product.git",
            "revision": f"{CI_COMMIT_SHA}/integrates/back/packages",
        },
    }
    requests.post(URL, headers=HEADERS, data=json.dumps(PAYLOAD))


def customize_bugsnag_error_reports(notification: Any) -> bool:
    """Handle for expected errors and customization"""
    bugsnag_remove_nix_hash(notification)
    ex_msg = str(notification.exception)

    notification.grouping_hash = ex_msg

    if isinstance(notification.exception, GraphQLError):
        return False
    if isinstance(notification.exception, UnavailabilityError):
        notification.unhandled = False
    if isinstance(notification.exception, DocumentNotFound):
        notification.severity = "info"

    return True


bugsnag.before_notify(customize_bugsnag_error_reports)
