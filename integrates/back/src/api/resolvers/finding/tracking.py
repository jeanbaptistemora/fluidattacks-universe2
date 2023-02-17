from .schema import (
    FINDING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    Tracking,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("tracking")
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> list[Tracking]:
    if not parent.approval:
        return []

    loaders: Dataloaders = info.context.loaders
    finding_vulns_loader = loaders.finding_vulnerabilities_released_nzr
    vulns = await finding_vulns_loader.load(parent.id)
    vulnerabilities_id = tuple(vuln.id for vuln in vulns)
    vulns_state = await loaders.vulnerability_historic_state.load_many(
        vulnerabilities_id
    )
    vulns_treatment = await loaders.vulnerability_historic_treatment.load_many(
        vulnerabilities_id
    )

    return findings_domain.get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
