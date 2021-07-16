from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
    Group,
    Vulnerability,
)
from decorators import (
    require_asm,
)
from findings.domain import (
    get_findings_by_group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import itertools
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


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, Finding]]:
    group_name: str = cast(str, parent["name"])

    findings: List[Dict[str, Finding]] = await get_findings_by_group(
        group_name
    )
    finding_ids = [finding["finding_id"] for finding in findings]

    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load_many(
        finding_ids
    )
    vulns_flatten: List[Vulnerability] = list(
        itertools.chain.from_iterable(vulns)
    )
    vulns_to_reattack: List[Vulnerability] = list(
        filter(filter_last_reattack_requested, vulns_flatten)
    )
    vulns_to_reattack = filter_open_vulnerabilities(vulns_to_reattack)

    return vulns_to_reattack
