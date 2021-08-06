from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    filter_last_reattack_requested,
)
from typing import (
    cast,
    Dict,
    List,
)
from vulnerabilities.domain import (
    filter_open_vulnerabilities,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, Finding]]:
    finding_id: str = cast(str, parent["id"])
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns_to_reattack: List[Vulnerability] = list(
        filter(filter_last_reattack_requested, vulns)
    )
    vulns_to_reattack = filter_open_vulnerabilities(vulns_to_reattack)

    return vulns_to_reattack
