from tempfile import NamedTemporaryFile
import json
import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql
from ariadne.asgi import (
    GraphQL,
    GQL_CONNECTION_INIT,
    GQL_CONNECTION_ACK,
    GQL_START,
    GQL_DATA,
    GQL_STOP,
    GQL_COMPLETE,
    GQL_CONNECTION_TERMINATE,
)

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from starlette.testclient import TestClient
from backend import util
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session


class SubscriptionTest(TestCase):

    async def _get_result(self, data):
        """Get result."""
        request = create_dummy_session('integratesmanager@gmail.com', 'fluid')
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result
