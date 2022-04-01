from aioextensions import (
    schedule,
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
from newutils import (
    logs as logs_utils,
)
from newutils.analytics import (
    mixpanel_track,
)
from newutils.token import (
    get_jwt_content,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class Operation(NamedTuple):
    name: str
    query: str
    variables: str


def _get_operation(data: Dict[str, Any]) -> Operation:
    return Operation(
        name=data.get("operationName") or "External (unnamed)",
        query=data.get("query", "").replace("\n", "") or "-",
        variables=data.get("variables") or "-",
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
    user_data = await get_jwt_content(request)
    await mixpanel_track(
        user_data["user_email"], f"API/{operation.name}", query=operation.query
    )


class IntegratesAPI(GraphQL):
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
