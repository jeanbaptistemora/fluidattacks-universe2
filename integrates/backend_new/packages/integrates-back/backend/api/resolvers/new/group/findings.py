# Standard
from typing import Any, cast, Dict, List, Optional

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import require_integrates
from backend.typing import Finding, Project as Group


@require_integrates
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any
) -> List[Finding]:
    group_name: str = cast(str, parent['name'])
    filters: Optional[Dict[str, Any]] = kwargs.get('filters')

    group_findings_loader: DataLoader = info.context.loaders['group_findings']
    finding_ids: List[str] = [
        finding['id']
        for finding in await group_findings_loader.load(group_name)
    ]

    finding_loader: DataLoader = info.context.loaders['finding']
    findings: List[Finding] = await finding_loader.load_many(finding_ids)

    if filters:
        return cast(
            List[Finding],
            await util.get_filtered_elements(findings, filters)
        )

    return findings
