from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding as FindingType,
    Vulnerability,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    filter_open_vulns,
    is_reattack_requested,
)
from typing import (
    Dict,
    List,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, FindingType]]:
    finding_id: str = parent.id
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulnerabilities_to_reattack: List[Vulnerability] = list(
        filter(is_reattack_requested, vulns)
    )
    vulnerabilities_to_reattack = filter_open_vulns(
        vulnerabilities_to_reattack
    )

    return vulnerabilities_to_reattack
