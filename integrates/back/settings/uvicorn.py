# IntegratesWorker class overrides uvicorn base worker to inject custom params

from uvicorn.workers import UvicornWorker


class IntegratesWorker(UvicornWorker):  # type: ignore

    CONFIG_KWARGS = {
        'interface': 'asgi3',
        'headers': [
            [
                'Pragma',
                'no-cache',
            ],
            [
                'WWW-Authenticate',
                'OAuth realm="Access to FLUIDIntegrates" charset="UTF-8"',
            ],
            [
                'X-XSS-Protection',
                '1; mode=block',
            ],
            [
                'X-Permitted-Cross-Domain-Policies',
                'master-only',
            ],
            [
                'X-Content-Type-Options',
                'nosniff',
            ],
            [
                'Expires',
                '0',
            ],
            [
                'Content-Security-Policy',
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                'localhost:* *.amazonaws.com *.cloudfront.net '
                '*.front.development.fluidattacks.com '
                '*.front.production.fluidattacks.com '
                '*.cloudflare.com *.cookiebot.com *.zdassets.com '
                '*.newrelic.com *.mxpnl.com *.pingdom.net '
                'bam.nr-data.net cdn.jsdelivr.net/npm/ '
                'cdn.headwayapp.co *.cloudflareinsights.com;',
            ],
            [
                'Accept-Encoding',
                'identity',
            ],
        ],
    }
