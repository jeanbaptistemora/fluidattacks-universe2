from decimal import Decimal

import logging
import pytest
import os
from django.db import connections
from django.conf import settings
from moto import mock_dynamodb2
import boto3
from boto3.dynamodb.conditions import Key

from backend.dal import finding

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)
