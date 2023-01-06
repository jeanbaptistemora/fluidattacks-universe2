from api import (
    Operation,
)
from api.extensions.constants import (
    VALID_ATTR_VALUE_TYPES,
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
from graphql.pyutils import (
    is_awaitable,
)
from opentelemetry import (
    trace,
)
from typing import (
    Any,
)


class FastExtension(Extension):
    """
    Resolve using a faster function to check for async resolvers

    Pending contribution to upstream
    https://github.com/graphql-python/graphql-core/issues/54
    """

    async def resolve(
        self,
        next_: Resolver,
        obj: Any,
        info: GraphQLResolveInfo,
        **kwargs: Any,
    ) -> Any:
        result = next_(obj, info, **kwargs)
        if is_awaitable(result):
            result = await result
        return result


def format_attributes(attributes: dict[str, Any]) -> dict[str, Any]:
    return {
        key: (
            str(value) if type(value) not in VALID_ATTR_VALUE_TYPES else value
        )
        for key, value in attributes.items()
    }


class OpenTelemetryExtension(FastExtension):
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
        operation_span.set_attributes(format_attributes(operation.variables))

    async def resolve(
        self,
        next_: Resolver,
        obj: Any,
        info: GraphQLResolveInfo,
        **kwargs: Any,
    ) -> Any:
        path = "/".join(str(element) for element in format_path(info.path))

        if should_trace(info):
            with self.tracer.start_as_current_span(
                attributes=format_attributes(kwargs),
                name=path,
            ):
                return await super().resolve(next_, obj, info, **kwargs)

        return await super().resolve(next_, obj, info, **kwargs)
