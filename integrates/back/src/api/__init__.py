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
from sentry_sdk import (
    configure_scope,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Dict,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


async def _log_request(request: Request, data: Dict[str, Any]) -> None:
    """
    Sends API operation metadata to cloud logging services for
    analytical purposes.
    """
    name: str = data.get("operationName") or "External (unnamed)"
    query: str = data.get("query", "").replace("\n", "") or "-"
    variables: str = data.get("variables") or "-"

    with configure_scope() as scope:
        scope.transaction = name
    logs_utils.cloudwatch_log(
        request,
        f"API: {name} with parameters {variables}. Complete query: {query}",
    )
    user_data = await get_jwt_content(request)
    await mixpanel_track(user_data["user_email"], f"API/{name}", query=query)


class IntegratesAPI(GraphQL):
    async def get_context_for_request(self, request: Request) -> Request:
        return apply_context_attrs(request)

    async def extract_data_from_request(
        self, request: Request
    ) -> Dict[str, Any]:
        """Hook before the execution process begins"""
        data: Dict[str, Any] = await super().extract_data_from_request(request)
        schedule(_log_request(request, data))

        return data
