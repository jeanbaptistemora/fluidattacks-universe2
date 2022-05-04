# IntegratesWorker class overrides uvicorn base worker to inject custom params
from uvicorn import (
    workers,
)


class IntegratesWorker(  # pylint: disable=too-few-public-methods
    workers.UvicornWorker
):

    CONFIG_KWARGS = {
        "interface": "asgi3",
        "headers": [
            ["server", "None"],
            [
                "Accept-Encoding",
                "identity",
            ],
            [
                "Referrer-Policy",
                "strict-origin-when-cross-origin",
            ],
            [
                "WWW-Authenticate",
                'OAuth realm="Access to FLUIDIntegrates" charset="UTF-8"',
            ],
            [
                "X-Permitted-Cross-Domain-Policies",
                "master-only",
            ],
            [
                "X-Content-Type-Options",
                "nosniff",
            ],
            [
                "X-XSS-Protection",
                "0",
            ],
            [
                "Content-Security-Policy",
                "script-src "
                "'self' "
                "'unsafe-inline' "
                "localhost:* "
                "fluidattacks.matomo.cloud "
                "cdn.announcekit.app "
                "bam-cell.nr-data.net "
                "bam.nr-data.net "
                "cdn.jsdelivr.net/npm/ "
                "d2yyd1h5u9mauk.cloudfront.net "
                "cdnjs.cloudflare.com/ajax/libs/d3/ "
                "js-agent.newrelic.com "
                "*.front.development.fluidattacks.com "
                "*.front.production.fluidattacks.com "
                "*.cookiebot.com "
                "*.zdassets.com "
                "*.mxpnl.com "
                "*.pingdom.net "
                "*.cloudflareinsights.com; "
                "frame-ancestors "
                "'self'; "
                "object-src "
                "'none'; "
                "upgrade-insecure-requests;",
            ],
            [
                "Permissions-Policy",
                "geolocation=(self), "
                "midi=(self), "
                "push=(self), "
                "sync-xhr=(self), "
                "microphone=(self), "
                "camera=(self), "
                "magnetometer=(self), "
                "gyroscope=(self), "
                "speaker=(self), "
                "vibrate=(self), "
                "fullscreen=(self), "
                "payment=(self) ",
            ],
        ],
    }
