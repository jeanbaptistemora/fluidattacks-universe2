from gunicorn.arbiter import (
    Arbiter,
)
from settings.uvicorn import (
    IntegratesWorker,
)
from telemetry import (
    instrumentation,
)


def post_fork(_arbiter: Arbiter, _worker: IntegratesWorker):
    instrumentation.initialize()
