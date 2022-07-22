from context import (
    FI_ENVIRONMENT,
    FI_NEW_RELIC_LICENSE_KEY,
)
from opentelemetry import (
    trace,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    Compression,
    OTLPSpanExporter,
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
    DEPLOYMENT_ENVIRONMENT,
    Resource,
    SERVICE_NAME,
)
from opentelemetry.sdk.trace import (
    TracerProvider,
)
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from starlette.applications import (
    Starlette,
)
from telemetry.aiobotocore import (
    AioBotocoreInstrumentor,
)


def instrument(app: Starlette) -> None:
    """
    Initializes the OpenTelemetry instrumentation

    Automatic instrumentation was not suitable as it currently lacks support
    for servers that fork processes like gunicorn
    https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model
    """
    resource = Resource.create(
        attributes={
            DEPLOYMENT_ENVIRONMENT: FI_ENVIRONMENT,
            SERVICE_NAME: "integrates",
        }
    )
    trace.set_tracer_provider(TracerProvider(resource=resource))

    if FI_ENVIRONMENT == "production":
        new_relic_exporter = OTLPSpanExporter(
            compression=Compression.Gzip,
            endpoint="https://otlp.nr-data.net:4318/v1/traces",
            headers={"api-key": FI_NEW_RELIC_LICENSE_KEY},
        )
        span_processor = BatchSpanProcessor(new_relic_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

    AioBotocoreInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    StarletteInstrumentor.instrument_app(app)
