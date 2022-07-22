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
from contextlib import (
    ExitStack,
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
        self.operation_context = ExitStack()
        self.tracer = trace.get_tracer(__name__)

    def request_started(self, context: Any) -> None:
        operation: Operation = context.operation
        operation_span = self.operation_context.enter_context(
            self.tracer.start_as_current_span(operation.name)
        )
        operation_span.set_attributes(operation.variables)

    def request_finished(self, _context: Any) -> None:
        if self.operation_context:
            self.operation_context.close()

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
                resolver_span.set_attributes(kwargs)

                return await super().resolve(next_, parent, info, **kwargs)

        return await super().resolve(next_, parent, info, **kwargs)
