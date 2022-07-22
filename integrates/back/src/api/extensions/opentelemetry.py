from api import (
    Operation,
)
from ariadne.contrib.tracing.utils import (
    format_path,
    should_trace,
)
from ariadne.types import (
    Extension,
    Resolver,
)
from graphql import (
    GraphQLResolveInfo,
)
from opentelemetry import (
    trace,
)
from typing import (
    Any,
)


class OpenTelemetryExtension(Extension):
    """
    OpenTelemetry extension for ariadne

    Pending contribution to upstream
    https://github.com/mirumee/ariadne/issues/649
    """

    def __init__(self) -> None:
        super().__init__()
        self.tracer = trace.get_tracer(__name__)

    def request_started(self, context: Any) -> None:
        operation: Operation = context.operation
        operation_span = trace.get_current_span()
        operation_span.update_name(operation.name)
        operation_span.set_attributes(
            {key: str(value) for key, value in operation.variables.items()}
        )

    async def resolve(
        self,
        next_: Resolver,
        parent: Any,
        info: GraphQLResolveInfo,
        **kwargs: Any,
    ) -> Any:
        path = "/".join(str(element) for element in format_path(info.path))

        if should_trace(info):
            with self.tracer.start_as_current_span(path) as resolver_span:
                if kwargs:
                    resolver_span.set_attributes(kwargs)

                return await super().resolve(next_, parent, info, **kwargs)

        return await super().resolve(next_, parent, info, **kwargs)
