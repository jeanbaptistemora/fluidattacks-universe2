from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
    Group,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    utils,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: Any
) -> List[Finding]:
    # pylint: disable=unsubscriptable-object
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
