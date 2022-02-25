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
import newrelic.agent
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
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


async def _log_request(
    request: Request,
    name: str,
    query: str,
    variables: str,
) -> None:
    """
    Sends API operation metadata to cloud logging services for
    analytical purposes.
    """
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
        name: str = data.get("operationName") or "External (unnamed)"
        query: str = data.get("query", "").replace("\n", "") or "-"
        variables: str = data.get("variables") or "-"

        newrelic.agent.set_transaction_name(name, "GraphQL")
        newrelic.agent.add_framework_info("GraphQL")
        schedule(_log_request(request, name, query, variables))

        return data
