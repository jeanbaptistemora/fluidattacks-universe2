import os
import logging.config
from logging import LogRecord
from boto3.session import Session

from backend_new import settings

from __init__ import (
    FI_AWS_CLOUDWATCH_ACCESS_KEY,
    FI_AWS_CLOUDWATCH_SECRET_KEY
)


AWS_ACCESS_KEY_ID = FI_AWS_CLOUDWATCH_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = FI_AWS_CLOUDWATCH_SECRET_KEY  # noqa
AWS_REGION_NAME = 'us-east-1'

BOTO3_SESSION = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
    region_name=AWS_REGION_NAME
)


# pylint: disable=too-few-public-methods
class RequireDebugFalse(logging.Filter):

    def filter(self, _: LogRecord) -> bool:
        return not settings.DEBUG


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': RequireDebugFalse
        },
    },
    'formatters': {
        'level_message_extra': {
            'format': '[{levelname}] {message}, extra={extra}',
            'style': '{',
        },
    },
    'handlers': {
        'bugsnag': {
            'extra_fields': {'extra': ['extra']},
            'class': 'bugsnag.handlers.BugsnagHandler',
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'level_message_extra',
        },
        'watchtower': {
            'boto3_session': BOTO3_SESSION,
            'class': 'watchtower.CloudWatchLogHandler',
            'level': 'INFO',
            'log_group': 'FLUID',
            'filters': ['require_debug_false'],
            'stream_name': 'FLUIDIntegrates',

            # Since LogGroup already exists, it was causing a
            # ThrottlingException error that resulted in 'unable to configure
            # watchtower'
            'create_log_group': False,
        },
    },
    'loggers': {
        'app': {
            'handlers': ['bugsnag', 'console'],
            'level': 'INFO'
        },
        'backend': {
            'handlers': ['bugsnag', 'console'],
            'level': 'INFO'
        },
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'transactional': {
            'handlers': ['console', 'watchtower'],
            'level': 'INFO'
        }
    }
}

NOEXTRA = {'extra': {'extra': None}}

# Force logging to load the config right away
# This is important otherwise loggers are not going to work in CI jobs
logging.config.dictConfig(LOGGING)
