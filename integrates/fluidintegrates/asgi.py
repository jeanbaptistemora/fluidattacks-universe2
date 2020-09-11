"""ASGI config for fluidintegrates project."""
import os

import django
import newrelic.agent

from django.conf import settings  # noqa: E402

# Init New Relic agent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fluidintegrates.settings")
django.setup()
NEW_RELIC_CONF_FILE = os.path.join(settings.BASE_DIR, 'newrelic.ini')
newrelic.agent.initialize(NEW_RELIC_CONF_FILE)

from django.urls import re_path  # noqa: E402
from uvicorn.workers import UvicornWorker  # noqa: E402

from ariadne.asgi import GraphQL  # noqa: E402

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.http import AsgiHandler  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402


from backend.api.schema import SCHEMA  # noqa: E402


# pylint: disable=too-few-public-methods
class AsgiHandlerWithNewrelic(AsgiHandler):
    def get_response(self, request):
        headers = None
        if "headers" in request.scope and isinstance(request.scope["headers"],
                                                     dict):
            headers = request.scope['headers']

        # https://docs.newrelic.com/docs/agents/python-agent/python-agent-api/webtransaction
        # instance of channels/handler.py `AsgiRequest`
        get_response_custom = newrelic.agent.WebTransactionWrapper(
            super().get_response,
            scheme=request.scheme,
            host=request.get_host(),
            port=request.get_port(),
            request_method=request.method,
            request_path=request.path,
            query_string=request.META.get('QUERY_STRING'),
            headers=headers
        )
        return get_response_custom(request)


class DjangoChannelsGraphQL(GraphQL):
    def __call__(self, scope) -> None:
        async def handle(receive, send):
            await \
                super(DjangoChannelsGraphQL, self).__call__(
                    scope, receive, send)
        return handle


APP = ProtocolTypeRouter({
    'http': AsgiHandlerWithNewrelic,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'^/?api/?\.*$',
                        DjangoChannelsGraphQL(
                            SCHEMA, debug=settings.DEBUG)),
                re_path(r'api',
                        DjangoChannelsGraphQL(
                            SCHEMA, debug=settings.DEBUG)),
            ])
    )
})


class IntegratesWorker(UvicornWorker):
    """Override worker to inject custom params."""

    CONFIG_KWARGS = {
        'loop': 'uvloop',
        'http': 'httptools',
        'root_path': '',
        'interface': 'asgi2',
        'log_level': 'info',
        'headers': [
            [
                'Pragma',
                'no-cache'
            ],
            [
                'WWW-Authenticate',
                'OAuth realm="Access to FLUIDIntegrates" charset="UTF-8"'
            ],
            [
                'X-XSS-Protection',
                '1; mode=block'
            ],
            [
                'X-Permitted-Cross-Domain-Policies',
                'master-only'
            ],
            [
                'X-Content-Type-Options',
                'nosniff'
            ],
            [
                'Expires',
                '0'
            ],
            [
                'Content-Security-Policy',
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                'localhost:* *.amazonaws.com *.cloudfront.net '
                '*.cloudflare.com *.cookiebot.com *.zdassets.com '
                '*.newrelic.com *.mxpnl.com *.pingdom.net '
                'https://d2yyd1h5u9mauk.cloudfront.net '
                'cdn.jsdelivr.net/npm/ cdn.headwayapp.co;'
            ],
            [
                'Accept-Encoding',
                'identity'
            ],
        ],
    }
