# Standard
from collections import defaultdict
from typing import Any, Dict

# Third party
import newrelic.agent
from ariadne.asgi import GraphQL
from django.utils.decorators import method_decorator
from starlette.requests import Request
from starlette.responses import Response

# Local
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader


def apply_context_attrs(context: Request) -> Request:
    setattr(context, 'loaders', {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'finding_vulns': FindingVulnsLoader(),
        'group': GroupLoader(),
        'group_drafts': GroupDraftsLoader(),
        'group_findings': GroupFindingsLoader(),
        'group_roots': GroupRootsLoader(),
        'vulnerability': VulnerabilityLoader()
    })
    setattr(context, 'store', defaultdict(lambda: None))

    return context


class IntegratesAPI(GraphQL):
    async def get_context_for_request(self, request: Request) -> Request:
        return apply_context_attrs(request)

    async def extract_data_from_request(
        self,
        request: Request
    ) -> Dict[str, Any]:
        """Apply configs for performance tracking"""
        data: Dict[str, Any] = await super().extract_data_from_request(request)

        name: str = data.get('operationName', 'External (unnamed)')
        newrelic.agent.set_transaction_name(f'api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))

        return data

    @method_decorator(newrelic.agent.web_transaction())
    async def graphql_http_server(self, request: Request) -> Response:
        return await super().graphql_http_server(request)
