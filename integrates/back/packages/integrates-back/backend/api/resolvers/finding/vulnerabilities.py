# Standard
from functools import (
    partial,
)
from typing import cast, Dict, List, Optional

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.domain import vulnerability as vuln_domain
from backend.typing import Finding, Vulnerability


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Vulnerability]:
    vulnerabilities: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='vulns',
        id=cast(Dict[str, str], parent)['id'],
    )

    state: Optional[str] = kwargs.get('state')

    vulnerabilities = vuln_domain.filter_non_confirmed_zero_risk_vuln(
        vulnerabilities
    )

    if state:
        vulnerabilities = [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability['current_state'] == state
        ]

    return vulnerabilities


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)['id']

    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vuln_domain.filter_non_confirmed_zero_risk_vuln(vulns)

    return vulns
