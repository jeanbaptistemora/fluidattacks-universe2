# Standard
from typing import Any, cast, Dict, List, Optional

# Third party
from aiodataloader import DataLoader
from graphql.language.ast import SelectionSetNode
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.api.resolvers import finding as old_resolver
from backend.decorators import require_integrates
from backend.typing import Finding, Project as Group
from backend.utils import aio


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
        findings = cast(
            List[Finding],
            await util.get_filtered_elements(findings, filters)
        )

    return cast(
        List[Finding],
        await aio.materialize(
            old_resolver.resolve(
                info,
                cast(Dict[str, str], finding)['id'],
                as_field=True,
                selection_set=cast(
                    SelectionSetNode,
                    info.field_nodes[0].selection_set
                )
            )
            for finding in findings
        )
    )
