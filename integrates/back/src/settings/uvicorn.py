from gunicorn.reloader import (
    reloader_engines,
)
import os
import time
from uvicorn import (
    workers,
)


class IntegratesWorker(workers.UvicornWorker):

    CONFIG_KWARGS = {
        "interface": "asgi3",
        "headers": [
            ["server", "None"],
            [
                "Accept-Encoding",
                "identity",
            ],
            ["Cross-Origin-Opener-Policy", "same-origin"],
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
            ["Cache-Control", "must-revalidate, no-cache, no-store"],
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
                "cdnjs.cloudflare.com/ajax/libs/c3/ "
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

    def init_process(self) -> None:
        """
        Needed while some patches arrive upstream
        https://github.com/benoitc/gunicorn/pull/2820
        """
        if self.cfg.reload:
            self.cfg.set("reload", False)

            def changed(fname: str) -> None:
                self.log.info("Worker reloading: %s modified", fname)
                self.alive = False
                os.write(self.PIPE[1], b"1")
                self.cfg.worker_int(self)
                time.sleep(0.1)
                # pylint: disable=protected-access
                os._exit(0)

            reloader_cls = reloader_engines[self.cfg.reload_engine]
            self.reloader = reloader_cls(
                callback=changed,
                extra_files=self.cfg.reload_extra_files,
            )

        super().init_process()
