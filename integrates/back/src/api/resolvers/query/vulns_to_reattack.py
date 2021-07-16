from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Finding,
    Vulnerability,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from findings.domain import (
    get_findings_by_group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups.domain import (
    get_active_groups,
)
import itertools
from newutils.vulnerabilities import (
    filter_last_reattack_requested,
)
from typing import (
    Dict,
    List,
)
from vulnerabilities.domain import (
    filter_open_vulnerabilities,
)


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> List[Dict[str, Finding]]:
    group_name = kwargs.get("group", "all")
    findings: List[List[Dict[str, Finding]]]

    if group_name == "all":
        groups = await get_active_groups()
        findings = list(
            await collect(get_findings_by_group(group) for group in groups)
        )
    else:
        findings = [await get_findings_by_group(group_name)]

    findings_flatten = list(itertools.chain.from_iterable(findings))
    finding_ids = [finding["finding_id"] for finding in findings_flatten]
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
