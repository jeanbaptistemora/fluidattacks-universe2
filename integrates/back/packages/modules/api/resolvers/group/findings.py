from typing import (
    Any,
    Dict,
    List,
    Optional,
    cast,
)

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Finding,
    Project as Group,
)
from decorators import require_integrates
from newutils import utils


@require_integrates
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: Any
) -> List[Finding]:
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    finding_loader: DataLoader = info.context.loaders.finding

    group_name: str = cast(str, parent["name"])
    filters: Optional[Dict[str, Any]] = kwargs.get("filters")
    finding_ids: List[str] = [
        finding["id"]
        for finding in await group_findings_loader.load(group_name)
    ]
    findings: List[Finding] = await finding_loader.load_many(finding_ids)

    if filters:
        return cast(
            List[Finding], await utils.get_filtered_elements(findings, filters)
        )
    return findings
