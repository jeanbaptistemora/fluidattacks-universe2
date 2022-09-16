# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_ENVIRONMENT,
    FI_NEW_RELIC_LICENSE_KEY,
)
from opentelemetry import (  # type: ignore
    metrics,
    trace,
)
from opentelemetry.exporter.otlp.proto.grpc import (  # type: ignore
    metric_exporter,
    trace_exporter,
)
from opentelemetry.exporter.otlp.proto.grpc.exporter import (
    Compression,
)
from opentelemetry.instrumentation.aiohttp_client import (  # type: ignore
    AioHttpClientInstrumentor,
)
from opentelemetry.instrumentation.redis import (  # type: ignore
    RedisInstrumentor,
)
from opentelemetry.instrumentation.requests import (  # type: ignore
    RequestsInstrumentor,
)
from opentelemetry.instrumentation.starlette import (  # type: ignore
    StarletteInstrumentor,
)
from opentelemetry.sdk.metrics import (  # type: ignore
    MeterProvider,
)
from opentelemetry.sdk.metrics.export import (  # type: ignore
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import (  # type: ignore
    DEPLOYMENT_ENVIRONMENT,
    Resource,
    SERVICE_NAME,
)
from opentelemetry.sdk.trace import (  # type: ignore
    TracerProvider,
)
from opentelemetry.sdk.trace.export import (  # type: ignore
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

    if FI_ENVIRONMENT == "production":
        span_exporter = trace_exporter.OTLPSpanExporter(
            compression=Compression.Gzip,
            endpoint="https://otlp.nr-data.net:4318/v1/traces",
            headers={"api-key": FI_NEW_RELIC_LICENSE_KEY},
        )
        span_processor = BatchSpanProcessor(
            max_queue_size=8192,
            span_exporter=span_exporter,
        )
        trace.set_tracer_provider(TracerProvider(resource=resource))
        trace.get_tracer_provider().add_span_processor(span_processor)

        metric_exporter_ = metric_exporter.OTLPMetricExporter(
            compression=Compression.Gzip,
            endpoint="https://otlp.nr-data.net:4318/v1/metrics",
            headers={"api-key": FI_NEW_RELIC_LICENSE_KEY},
        )
        metric_reader = PeriodicExportingMetricReader(metric_exporter_)
        metrics.set_meter_provider(
            MeterProvider(
                metric_readers=[metric_reader],
                resource=resource,
            )
        )

    AioBotocoreInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    StarletteInstrumentor.instrument_app(app)
