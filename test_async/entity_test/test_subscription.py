from tempfile import NamedTemporaryFile
import json
import os
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
from backend.api.schema import SCHEMA


class SubscriptionTest(TestCase):

    async def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesmanager@gmail.com'
        request.session['company'] = 'fluid'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    @pytest.mark.asyncio
    async def test_post_broadcast(self):
        """Check for post_broadcast_message mutation."""
        query = '''
            mutation {
                postBroadcastMessage(message: "Hello from unittesting"){
                    success
                }
            }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert result['data']['postBroadcastMessage']['success']

    def test_websocket_connection(self):
        """Test websocket consumer."""
        client = TestClient(GraphQL(SCHEMA))
        with client.websocket_connect("/api", "graphql-ws") as ws:
            ws.send_json({"type": GQL_CONNECTION_INIT})
            ws.send_json(
                {
                    "type": GQL_START,
                    "id": "test1",
                    "payload": {"query": "subscription { broadcast }"},
                }
            )
            response = ws.receive_json()
            assert response["type"] == GQL_CONNECTION_ACK
            response = ws.receive_json()
            assert response["type"] == GQL_DATA
            assert response["id"] == "test1"
            ws.send_json({"type": GQL_STOP, "id": "test1"})
            response = ws.receive_json()
            assert response["type"] in (GQL_COMPLETE, GQL_DATA)
            assert response["id"] == "test1"
            ws.send_json({"type": GQL_CONNECTION_TERMINATE})
