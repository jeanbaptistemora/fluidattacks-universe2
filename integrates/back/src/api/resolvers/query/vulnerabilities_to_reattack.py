from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Vulnerability,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
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
    List,
    Tuple,
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
) -> List[Vulnerability]:
    group_findings_loader: DataLoader = info.context.loaders.group_findings_new
    group_name = kwargs.get("group", "all")

    if group_name == "all":
        groups = await get_active_groups()
        findings: Tuple[
            Tuple[Finding, ...], ...
        ] = await group_findings_loader.load_many(groups)
    else:
        findings = await group_findings_loader.load_many([group_name])

    findings_flatten = list(itertools.chain.from_iterable(findings))
    finding_ids = [finding.id for finding in findings_flatten]
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load_many(
        finding_ids
    )
    vulns_flatten: List[Vulnerability] = list(
        itertools.chain.from_iterable(vulns)
    )
    vulnerabilities_to_reattack: List[Vulnerability] = list(
        filter(filter_last_reattack_requested, vulns_flatten)
    )
    vulnerabilities_to_reattack = filter_open_vulnerabilities(
        vulnerabilities_to_reattack
    )

    return vulnerabilities_to_reattack
