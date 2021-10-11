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
    tracking = []
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    if parent.approval:
        vulns = await finding_vulns_loader.load(parent.id)
        tracking = findings_domain.get_tracking_vulnerabilities(vulns)
    return tracking
