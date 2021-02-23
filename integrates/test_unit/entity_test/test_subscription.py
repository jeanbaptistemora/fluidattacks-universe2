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

from jose import jwt
from starlette.testclient import TestClient
from backend import util
from backend.api.schema import SCHEMA
from test_unit.utils import create_dummy_session


async def _get_result(data):
    """Get result."""
    request = await create_dummy_session('integratesmanager@gmail.com')
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result
