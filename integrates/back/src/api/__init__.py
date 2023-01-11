from api.validations.directives import (
    validate_directives,
)
from ariadne.asgi import (
    GraphQL,
)
from ariadne.asgi.handlers import (
    GraphQLHTTPHandler,
)
from custom_exceptions import (
    CustomBaseException,
)
from dataloaders import (
    apply_context_attrs,
)
from dynamodb.exceptions import (
    DynamoDbBaseException,
)
from graphql import (
    DocumentNode,
)
from newutils import (
    logs as logs_utils,
)
from starlette.requests import (
    Request,
)
import sys
from typing import (
    Any,
    NamedTuple,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class Operation(NamedTuple):
    name: str
    query: str
    variables: dict[str, Any]


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


class IntegratesAPI(GraphQL):  # pylint: disable=too-few-public-methods
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        hook_early_validations()


class IntegratesHTTPHandler(GraphQLHTTPHandler):
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
