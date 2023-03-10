import graphql
from graphql import (
    default_field_resolver,
    DocumentNode,
    ExecutionContext,
    FieldNode,
    get_operation_ast,
    GraphQLError,
    GraphQLField,
    GraphQLFieldResolver,
    GraphQLObjectType,
    OperationDefinitionNode,
    Source,
)
from graphql.execution.execute import (
    get_field_def,
)
from graphql.language.parser import (
    SourceType,
)

try:
    # Faster, but only available from 3.1.0 onwards
    from graphql.pyutils import (
        is_awaitable,
    )
except ImportError:
    from inspect import (  # type: ignore
        isawaitable as is_awaitable,
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
    cast,
    Collection,
    List,
    Optional,
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
            graphql.validation,
            "validate",
            self._patched_validate,
        )
        wrap_function_wrapper(
            graphql,
            "execute",
            self._patched_execute,
        )
        wrap_function_wrapper(
            graphql,
            "ExecutionContext.execute_field",
            self._patched_execute_field,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(graphql, "parse")
        unwrap(graphql.validation, "validate")
        unwrap(graphql, "execute")
        unwrap(graphql, "ExecutionContext.execute_field")

    def _patched_parse(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.parse") as span:
            source_arg: SourceType = args[0]
            _set_document_attr(span, source_arg)

            return original_func(*args, **kwargs)

    def _patched_validate(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.validate") as span:
            document_arg: DocumentNode = args[1]
            _set_document_attr(span, document_arg)

            errors = original_func(*args, **kwargs)
            _set_errors(span, errors)
            return errors

    def _patched_execute(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.execute") as span:
            document_arg: DocumentNode = args[1]
            _set_operation_attrs(span, document_arg)
            result = original_func(*args, **kwargs)

            if is_awaitable(result):

                async def await_result() -> Any:
                    with self._tracer.start_as_current_span(
                        "graphql.execute.await"
                    ) as span:
                        _set_operation_attrs(span, document_arg)
                        async_result = await result
                        _set_errors(span, async_result.errors)
                        return async_result

                return await_result()
            _set_errors(span, result.errors)
            return result

    def _patched_execute_field(
        self,
        original_func: Callable[..., Any],
        instance: ExecutionContext,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        parent_type_arg: GraphQLObjectType = args[0]
        field_nodes_arg: List[FieldNode] = args[2]
        field_node = field_nodes_arg[0]
        field = get_field_def(instance.schema, parent_type_arg, field_node)

        if _should_exclude_field(field, instance.operation):
            return original_func(*args, **kwargs)

        with self._tracer.start_as_current_span("graphql.resolve") as span:
            _set_field_attrs(span, field_node)
            result = original_func(*args, **kwargs)

            if is_awaitable(result):

                async def await_result() -> Any:
                    with self._tracer.start_as_current_span(
                        "graphql.resolve.await"
                    ) as span:
                        _set_field_attrs(span, field_node)
                        return await result

                return await_result()
            return result


def _format_source(obj: Union[DocumentNode, Source, str]) -> str:
    if isinstance(obj, str):
        value = obj
    elif isinstance(obj, Source):
        value = obj.body
    elif isinstance(obj, DocumentNode) and obj.loc:
        value = obj.loc.source.body
    else:
        value = ""

    return re.sub(r"\s+", " ", value).strip()


def _set_document_attr(
    span: Span, obj: Union[DocumentNode, Source, str]
) -> None:
    source = _format_source(obj)
    span.set_attribute("graphql.document", source)


def _set_operation_attrs(span: Span, document: DocumentNode) -> None:
    _set_document_attr(span, document)

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


def _set_errors(span: Span, errors: Optional[List[GraphQLError]]) -> None:
    if errors:
        for error in errors:
            span.record_exception(error)


def _set_field_attrs(span: Span, field_node: FieldNode) -> None:
    span.set_attribute("graphql.field.name", field_node.name.value)


def _is_default_resolver(resolver: Optional[GraphQLFieldResolver]) -> bool:
    # pylint: disable=comparison-with-callable
    return (
        # graphql-core
        resolver is None
        or resolver == default_field_resolver
        # ariadne
        or getattr(resolver, "_ariadne_alias_resolver", False)
        # strawberry
        or getattr(resolver, "_is_default", False)
    )


def _is_introspection_query(operation: OperationDefinitionNode) -> bool:
    selections = operation.selection_set.selections

    if selections:
        root_field = cast(FieldNode, selections[0])
        return root_field.name.value == "__schema"
    return False


def _should_exclude_field(
    field: GraphQLField, operation: OperationDefinitionNode
) -> bool:
    return _is_default_resolver(field.resolve) or _is_introspection_query(
        operation
    )
