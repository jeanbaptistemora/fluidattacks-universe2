from decimal import Decimal

import logging
import pytest
import os
from django.db import connections
from django.conf import settings
from moto import mock_dynamodb2
import boto3
from boto3.dynamodb.conditions import Key

from backend.domain import user as user_domain
from backend.dal import finding
from backend import util

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(autouse=True, scope='session')
def load_enforcers():
    """Load policies from DB into the enforcers."""
    user_domain.grant_user_level_role('unittest', 'admin')
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_GROUP_LEVEL_ASYNC)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_GROUP_LEVEL)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_USER_LEVEL_ASYNC)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_USER_LEVEL)


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)
