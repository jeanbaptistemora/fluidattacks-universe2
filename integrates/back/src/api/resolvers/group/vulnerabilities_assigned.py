from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.token import (
    get_jwt_content,
)
from newutils.vulnerabilities import (
    filter_open_vulns,
)
from typing import (
    Any,
    Dict,
    Tuple,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[Vulnerability, ...]:
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    user_data = await get_jwt_content(info.context)
    loaders: Dataloaders = info.context.loaders
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    finding_ids = [finding.id for finding in findings]
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        finding_ids
    )

    return tuple(
        vulnerability
        for vulnerability in filter_open_vulns(vulnerabilities)
        if vulnerability.treatment.assigned == user_data["user_email"]
    )
