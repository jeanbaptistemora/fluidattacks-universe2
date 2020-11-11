"""ASGI config for fluidintegrates project."""

# Standard
import os

# Initialize django (order matters)
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')
django.setup()

# Third party
import newrelic.agent   # noqa: E402
from channels.auth import AuthMiddlewareStack   # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter   # noqa: E402
from django.conf import settings   # noqa: E402
from django.core.asgi import get_asgi_application   # noqa: E402
from django.urls import re_path   # noqa: E402
from uvicorn.workers import UvicornWorker   # noqa: E402

# Local
from backend.api import IntegratesAPI   # noqa: E402
from backend.api.schema import SCHEMA   # noqa: E402


# Init New Relic agent
NEW_RELIC_CONF_FILE = os.path.join(settings.BASE_DIR, 'newrelic.ini')
newrelic.agent.initialize(NEW_RELIC_CONF_FILE)

APP = newrelic.agent.ASGIApplicationWrapper(
    ProtocolTypeRouter({
        'http': URLRouter([
            re_path(r'^api/?', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
            re_path(r'', get_asgi_application())
        ]),
        'websocket': AuthMiddlewareStack(
            URLRouter([
                re_path(
                    r'^api/?',
                    IntegratesAPI(SCHEMA, debug=settings.DEBUG)
                ),
            ])
        )
    })
)


class IntegratesWorker(UvicornWorker):
    """Override worker to inject custom params."""

    CONFIG_KWARGS = {
        'loop': 'uvloop',
        'http': 'httptools',
        'root_path': '',
        'interface': 'asgi3',
        'log_level': 'info',
        'headers': [
            [
                'Pragma',
                'no-cache'
            ],
            [
                'server',
                'None'
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
                'https://d2yyd1h5u9mauk.cloudfront.net bam.nr-data.net '
                'js-agent.nr-assets.net cdn.jsdelivr.net/npm/ '
                'cdn.headwayapp.co;'
            ],
            [
                'Accept-Encoding',
                'identity'
            ],
        ],
    }
