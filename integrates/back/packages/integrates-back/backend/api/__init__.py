# Standard libraries
from collections import (
    defaultdict,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional
)

# Third party libraries
import newrelic.agent
from ariadne.asgi import GraphQL
from starlette.requests import Request
from starlette.responses import Response

# Local libraries
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.finding_vulns_non_deleted import (
    FindingVulnsNonDeletedLoader
)
from backend.api.dataloaders.finding_vulns_non_zero_risk import (
    FindingVulnsNonZeroRiskLoader
)
from backend.api.dataloaders.finding_vulns_only_zero_risk import (
    FindingVulnsOnlyZeroRiskLoader
)
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_active import GroupActiveLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.group_findings_non_deleted import (
    GroupFindingsNonDeletedLoader
)
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.api.dataloaders.group_stakeholders import GroupStakeholdersLoader
from backend.api.dataloaders.group_stakeholders_non_fluid import (
    GroupStakeholdersNonFluidLoader
)
from backend.api.dataloaders.organization_stakeholders import (
    OrganizationStakeholdersLoader
)
from backend.api.dataloaders.vulnerability import VulnerabilityLoader

from back import settings

newrelic.agent.initialize(settings.NEW_RELIC_CONF_FILE)


class Dataloaders(NamedTuple):
    event: EventLoader
    finding: FindingLoader
    finding_vulns: FindingVulnsLoader  # All vulns except deleted
    finding_vulns_all: FindingVulnsNonDeletedLoader  # All vulns
    finding_vulns_nzr: FindingVulnsNonZeroRiskLoader  # Standard call
    finding_vulns_zr: FindingVulnsOnlyZeroRiskLoader
    group: GroupActiveLoader
    group_all: GroupLoader  # Used only by analytics. Retrieves all groups
    group_drafts: GroupDraftsLoader
    group_findings: GroupFindingsNonDeletedLoader  # Non deleted findings
    group_findings_all: GroupFindingsLoader  # All findings
    group_roots: GroupRootsLoader
    group_stakeholders: GroupStakeholdersLoader
    group_stakeholders_nf: GroupStakeholdersNonFluidLoader
    organization_stakeholders: OrganizationStakeholdersLoader
    vulnerability: VulnerabilityLoader


def get_new_context() -> Dataloaders:
    group_loader = GroupLoader()
    group_findings_loader = GroupFindingsLoader()
    group_stakeholders_loader = GroupStakeholdersLoader()
    finding_vulns_loader = FindingVulnsLoader()
    finding_vulns_non_deleted_loader = \
        FindingVulnsNonDeletedLoader(finding_vulns_loader)
    finding_vulns_nzr_loader = \
        FindingVulnsNonZeroRiskLoader(finding_vulns_non_deleted_loader)
    finding_vulns_zr_loader = \
        FindingVulnsOnlyZeroRiskLoader(finding_vulns_loader)

    return Dataloaders(
        event=EventLoader(),
        finding=FindingLoader(),
        finding_vulns=finding_vulns_non_deleted_loader,
        finding_vulns_all=finding_vulns_loader,
        finding_vulns_nzr=finding_vulns_nzr_loader,
        finding_vulns_zr=finding_vulns_zr_loader,
        group=GroupActiveLoader(group_loader),
        group_all=group_loader,
        group_drafts=GroupDraftsLoader(),
        group_findings=GroupFindingsNonDeletedLoader(group_findings_loader),
        group_findings_all=group_findings_loader,
        group_roots=GroupRootsLoader(),
        group_stakeholders=group_stakeholders_loader,
        group_stakeholders_nf=GroupStakeholdersNonFluidLoader(
            group_stakeholders_loader
        ),
        organization_stakeholders=OrganizationStakeholdersLoader(),
        vulnerability=VulnerabilityLoader()
    )


def apply_context_attrs(
    context: Request,
    loaders: Optional[Dataloaders] = None
) -> Request:
    setattr(context, 'loaders', loaders if loaders else get_new_context())
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
