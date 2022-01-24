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
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Dict,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class IntegratesAPI(GraphQL):
    async def get_context_for_request(self, request: Request) -> Request:
        return apply_context_attrs(request)

    async def extract_data_from_request(
        self, request: Request
    ) -> Dict[str, Any]:
        """Apply configs for performance tracking"""
        data: Dict[str, Any] = await super().extract_data_from_request(request)

        name: str = data.get("operationName", "External (unnamed)")
        query: str = data.get("query", "-").replace("\n", "")
        variables: str = data.get("variables", "-")

        logs_utils.cloudwatch_log(
            request,
            f"API: {name} with parameters {variables}."
            f"Complete query: {query}",
        )

        return data
