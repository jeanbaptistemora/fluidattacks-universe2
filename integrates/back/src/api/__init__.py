# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    schedule,
)
from api.validations.directives import (
    validate_directives,
)
from ariadne.asgi import (
    GraphQL,
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
    Dict,
    NamedTuple,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class Operation(NamedTuple):
    name: str
    query: str
    variables: Dict[str, Any]


def _get_operation(data: Dict[str, Any]) -> Operation:
    return Operation(
        name=data.get("operationName") or "External (unnamed)",
        query=data.get("query", "").replace("\n", "") or "-",
        variables=data.get("variables") or {},
    )


async def _log_request(request: Request, operation: Operation) -> None:
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
    original_parse = ariadne_graphql.parse_query  # type: ignore

    def before_parse(query: str) -> DocumentNode:
        validate_directives(query)

        return original_parse(query)

    ariadne_graphql.parse_query = before_parse  # type: ignore


class IntegratesAPI(GraphQL):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        hook_early_validations()

    async def get_context_for_request(self, request: Request) -> Request:
        data: Dict[str, Any] = await super().extract_data_from_request(request)
        operation = _get_operation(data)
        context = apply_context_attrs(request)
        setattr(context, "operation", operation)

        return context

    async def extract_data_from_request(
        self, request: Request
    ) -> Dict[str, Any]:
        """Hook before the execution process begins"""
        data: Dict[str, Any] = await super().extract_data_from_request(request)
        operation = _get_operation(data)

        schedule(_log_request(request, operation))

        return data
