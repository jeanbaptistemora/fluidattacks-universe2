import graphql
from graphql import (
    DocumentNode,
    get_operation_ast,
    Source,
)
from graphql.language.parser import (
    SourceType,
)
from inspect import (
    isawaitable,
)
from opentelemetry.instrumentation.instrumentor import (  # type: ignore
    BaseInstrumentor,
)
from opentelemetry.instrumentation.utils import (
    unwrap,
)
from opentelemetry.trace import (
    get_tracer,
    Span,
)
import re
from typing import (
    Any,
    Callable,
    Collection,
    Union,
)
from wrapt import (
    wrap_function_wrapper,
)


class GraphQLCoreInstrumentor(BaseInstrumentor):
    """
    OpenTelemetry instrumentor for graphql-core

    Pending contribution to upstream
    https://github.com/open-telemetry/opentelemetry-python-contrib/
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return ("graphql-core ~= 3.0",)

    def _instrument(self, **kwargs: Any) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._tracer = get_tracer(__name__)

        wrap_function_wrapper(
            graphql,
            "parse",
            self._patched_parse,
        )
        wrap_function_wrapper(
            graphql,
            "execute",
            self._patched_execute,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(graphql, "parse")
        unwrap(graphql, "execute")

    def _patched_parse(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.parse") as span:
            source_arg: SourceType = args[0]
            source = _format_source(source_arg)
            span.set_attribute("graphql.document", source)

            return original_func(*args, **kwargs)

    def _patched_execute(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.execute") as span:
            document_arg: DocumentNode = args[1]
            _set_execute_span(span, document_arg)

            result = original_func(*args, **kwargs)

            if isawaitable(result):

                async def await_result() -> Any:
                    with self._tracer.start_as_current_span(
                        "graphql.execute.await"
                    ) as span:
                        _set_execute_span(span, document_arg)
                        return await result

                return await_result()
            return result


def _set_execute_span(span: Span, document: DocumentNode) -> None:
    if document.loc:
        source = _format_source(document.loc.source)
        span.set_attribute("graphql.document", source)

    operation_definition = get_operation_ast(document)

    if operation_definition:
        span.set_attribute(
            "graphql.operation.type",
            operation_definition.operation.value,
        )

        if operation_definition.name:
            span.set_attribute(
                "graphql.operation.name",
                operation_definition.name.value,
            )


def _format_source(source: Union[Source, str]) -> str:
    if isinstance(source, str):
        value = source
    elif isinstance(source, Source):
        value = source.body
    else:
        value = ""

    return re.sub(r"\s+", " ", value).strip()
