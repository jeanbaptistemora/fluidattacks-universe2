from api import (
    Operation,
)
from ariadne.contrib.tracing.utils import (
    should_trace,
)
from ariadne.types import (
    Extension,
    Resolver,
)
from ddtrace import (
    tracer,
)
from graphql import (
    GraphQLResolveInfo,
)
from inspect import (
    isawaitable,
)
from typing import (
    Any,
)


class DatadogTracingExtension(Extension):
    def __init__(self) -> None:
        super().__init__()
        self.operation_span = None

    def request_started(self, context: Any) -> None:
        operation: Operation = context.operation
        operation_span = tracer.trace(operation.name, service="API")
        operation_span.set_tags(operation._asdict())
        self.operation_span = operation_span

    def request_finished(self, _context: Any) -> None:
        if self.operation_span:
            self.operation_span.finish()

    # pylint:disable=arguments-renamed
    # Disabled due to https://gitlab.com/fluidattacks/product/-/issues/6088
    async def resolve(
        self,
        next_: Resolver,
        parent_: Any,
        info: GraphQLResolveInfo,
        **kwargs: Any,
    ) -> Any:
        if not should_trace(info):
            result = next_(parent_, info, **kwargs)
            if isawaitable(result):
                return await result
            return result

        path = "/".join(
            field for field in info.path.as_list() if isinstance(field, str)
        )

        with tracer.trace(path) as resolver_span:
            resolver_span.set_tags(dict(args=kwargs))
            result = next_(parent_, info, **kwargs)
            if isawaitable(result):
                return await result
            return result
