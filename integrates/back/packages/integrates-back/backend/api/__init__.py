# Standard
from collections import (
    defaultdict,
)
from typing import (
    Any,
    Dict,
    NamedTuple
)

# Third party
import newrelic.agent
from ariadne.asgi import GraphQL
from starlette.requests import Request
from starlette.responses import Response

# Local
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader

from back import settings

newrelic.agent.initialize(settings.NEW_RELIC_CONF_FILE)


class Dataloaders(NamedTuple):
    event: EventLoader
    finding: FindingLoader
    finding_vulns: FindingVulnsLoader
    group: GroupLoader
    group_drafts: GroupDraftsLoader
    group_findings: GroupFindingsLoader
    group_roots: GroupRootsLoader
    project: ProjectLoader  # used only by analytics. Needs refactor or rename
    vulnerability: VulnerabilityLoader


def get_new_context() -> Dataloaders:
    return Dataloaders(
        event=EventLoader(),
        finding=FindingLoader(),
        finding_vulns=FindingVulnsLoader(),
        group=GroupLoader(),
        group_drafts=GroupDraftsLoader(),
        group_findings=GroupFindingsLoader(),
        group_roots=GroupRootsLoader(),
        project=ProjectLoader(),
        vulnerability=VulnerabilityLoader()
    )


def apply_context_attrs(context: Request) -> Request:
    setattr(context, 'loaders', get_new_context())
    setattr(context, 'store', defaultdict(lambda: None))

    return context


class IntegratesAPI(GraphQL):  # type: ignore
    async def get_context_for_request(self, request: Request) -> Request:
        return apply_context_attrs(request)

    async def extract_data_from_request(
        self,
        request: Request
    ) -> Dict[str, Any]:
        """Apply configs for performance tracking"""
        data: Dict[str, Any] = await super().extract_data_from_request(request)

        name: str = data.get('operationName', 'External (unnamed)')
        query: str = data.get('query', '-').replace('\n', '')
        variables: str = data.get('variables', '-')

        newrelic.agent.set_transaction_name(f'api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))
        util.cloudwatch_log(
            request,
            f'API: {name} with parameters {variables}. Complete query: {query}'
        )

        return data

    @newrelic.agent.web_transaction()  # type: ignore
    async def graphql_http_server(self, request: Request) -> Response:
        return await super().graphql_http_server(request)
