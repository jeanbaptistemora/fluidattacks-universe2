from .enums import (
    ENUMS,
)
from .extensions.opentelemetry import (
    OpenTelemetryExtension,
)
from .resolvers import (
    TYPES,
)
from .scalars import (
    SCALARS,
)
from .types import (
    Operation,
)
from .unions import (
    UNIONS,
)
from .validations.characters import (
    validate_characters,
)
from .validations.directives import (
    validate_directives,
)
from .validations.query_breadth import (
    QueryBreadthValidation,
)
from .validations.query_depth import (
    QueryDepthValidation,
)
from .validations.variables_validation import (
    variables_check,
)
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.asgi import (
    GraphQL,
)
from ariadne.asgi.handlers import (
    GraphQLHTTPHandler,
)
from ariadne.types import (
    ExtensionList,
)
from dataloaders import (
    apply_context_attrs,
)
from graphql import (
    ASTValidationRule,
    DocumentNode,
)
from newutils import (
    logs as logs_utils,
)
import os
from settings.various import (
    DEBUG,
)
from starlette.requests import (
    Request,
)
import sys
from typing import (
    Any,
)


def _get_operation(data: dict[str, Any]) -> Operation:
    return Operation(
        name=data.get("operationName") or "External (unnamed)",
        query=data.get("query", "").replace("\n", "") or "-",
        variables=data.get("variables") or {},
    )


def _log_request(request: Request, operation: Operation) -> None:
    """
    Sends API operation metadata to cloud logging services for
    analytical purposes.
    """
    logs_utils.cloudwatch_log(
        request,
        f"API: {operation.name} with parameters {operation.variables}. "
        f"Complete query: {operation.query}",
    )


def hook_early_validations() -> None:
    """
    Hook into the execution process

    Warning: This is intended as a temporal workaround while some patches
    arrive upstream.
    """
    ariadne_graphql = sys.modules["ariadne.graphql"]
    original_parse = ariadne_graphql.parse_query

    def before_parse(query: str) -> DocumentNode:
        validate_directives(query)

        return original_parse(query)

    ariadne_graphql.parse_query = before_parse  # type: ignore


class IntegratesAPIHTTPHandler(GraphQLHTTPHandler):
    async def get_context_for_request(self, request: Request) -> Request:
        data: dict[str, Any] = await super().extract_data_from_request(request)
        operation = _get_operation(data)
        context = apply_context_attrs(request)
        setattr(context, "operation", operation)

        return context

    async def extract_data_from_request(
        self, request: Request
    ) -> dict[str, Any]:
        """Hook before the execution process begins"""
        data: dict[str, Any] = await super().extract_data_from_request(request)
        operation = _get_operation(data)

        _log_request(request, operation)

        return data


def get_validation_rules(
    context_value: Any | None,
    _document: DocumentNode,
    _data: dict[Any, Any],
) -> tuple[type[ASTValidationRule], ...]:
    return (  # type: ignore
        QueryBreadthValidation,
        QueryDepthValidation,
        validate_characters(context_value),
        variables_check(context_value),
    )


API_EXTENSIONS: ExtensionList = [
    OpenTelemetryExtension,
]
API_PATH = os.path.dirname(__file__)
SDL_CONTENT = "\n".join(
    [
        load_schema_from_path(os.path.join(API_PATH, module))
        for module in os.listdir(API_PATH)
        if os.path.isdir(os.path.join(API_PATH, module))
    ]
)
SCHEMA = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    *UNIONS,
    snake_case_fallback_resolvers,
)


class IntegratesAPI(GraphQL):  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        super().__init__(
            schema=SCHEMA,
            debug=DEBUG,
            http_handler=IntegratesAPIHTTPHandler(),
            validation_rules=get_validation_rules,
        )
        hook_early_validations()
