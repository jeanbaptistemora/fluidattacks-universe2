from opentelemetry import (
    trace,
)
from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor,
)
from opentelemetry.instrumentation.redis import (
    RedisInstrumentor,
)
from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor,
)
from opentelemetry.instrumentation.starlette import (
    StarletteInstrumentor,
)
from opentelemetry.sdk.resources import (
    Resource,
    SERVICE_NAME,
)
from opentelemetry.sdk.trace import (
    TracerProvider,
)
from starlette.applications import (
    Starlette,
)


def instrument(app: Starlette) -> None:
    """
    Initializes the OpenTelemetry instrumentation

    Automatic instrumentation was not suitable as it currently lacks support
    for servers that fork processes like gunicorn
    https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model
    """
    resource = Resource.create(attributes={SERVICE_NAME: "integrates"})
    trace.set_tracer_provider(TracerProvider(resource=resource))

    AioHttpClientInstrumentor().instrument()
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    StarletteInstrumentor.instrument_app(app)
