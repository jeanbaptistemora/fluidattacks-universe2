from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Tracking as TrackingItem,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[TrackingItem]:
    if not parent.approval:
        return []

    loaders = info.context.loaders
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    historic_state_loader: DataLoader = loaders.vulnerability_historic_state
    historic_treatment_loader: DataLoader = (
        loaders.vulnerability_historic_treatment
    )

    vulns = await finding_vulns_loader.load(parent.id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )

    return findings_domain.get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
