from typing import (
    Any,
    Dict,
)

import newrelic.agent
from ariadne.asgi import GraphQL
from starlette.requests import Request
from starlette.responses import Response

from back import settings
from dataloaders import apply_context_attrs
from newutils import logs as logs_utils


newrelic.agent.initialize(settings.NEW_RELIC_CONF_FILE)


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

        newrelic.agent.set_transaction_name(f"api:{name}")
        newrelic.agent.add_custom_parameters(tuple(data.items()))
        logs_utils.cloudwatch_log(
            request,
            f"API: {name} with parameters {variables}."
            f"Complete query: {query}",
        )

        return data

    @newrelic.agent.web_transaction()
    async def graphql_http_server(self, request: Request) -> Response:
        return await super().graphql_http_server(request)
