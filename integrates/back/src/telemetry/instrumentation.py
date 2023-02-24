from context import (
    FI_ENVIRONMENT,
)
from grpc import (
    Compression,
)
from opentelemetry import (
    metrics,
    trace,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor,
)
from opentelemetry.instrumentation.botocore import (
    BotocoreInstrumentor,
)
from opentelemetry.instrumentation.httpx import (
    HTTPXClientInstrumentor,
)
from opentelemetry.instrumentation.jinja2 import (
    Jinja2Instrumentor,
)
from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor,
)
from opentelemetry.instrumentation.starlette import (
    StarletteInstrumentor,
)
from opentelemetry.instrumentation.urllib3 import (
    URLLib3Instrumentor,
)
from opentelemetry.instrumentation.urllib import (
    URLLibInstrumentor,
)
from opentelemetry.sdk.metrics._internal import (
    MeterProvider,
)
from opentelemetry.sdk.metrics._internal.export import (
    PeriodicExportingMetricReader,
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


def initialize() -> None:
    """
    Initializes the OpenTelemetry exporters

    Automatic instrumentation was not suitable as it currently lacks support
    for servers that fork processes
    https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model
    """
    resource = Resource.create(
        attributes={
            DEPLOYMENT_ENVIRONMENT: FI_ENVIRONMENT,
            SERVICE_NAME: "integrates",
        }
    )

    span_exporter = OTLPSpanExporter(compression=Compression.Gzip)
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    metric_exporter = OTLPMetricExporter(compression=Compression.Gzip)
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(
        metric_readers=[metric_reader],
        resource=resource,
    )
    metrics.set_meter_provider(meter_provider)


def instrument(app: Starlette) -> None:
    """Initializes the OpenTelemetry instrumentation"""
    AioBotocoreInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    BotocoreInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    Jinja2Instrumentor().instrument()
    RequestsInstrumentor().instrument()
    StarletteInstrumentor.instrument_app(app)
    URLLibInstrumentor().instrument()
    URLLib3Instrumentor().instrument()
