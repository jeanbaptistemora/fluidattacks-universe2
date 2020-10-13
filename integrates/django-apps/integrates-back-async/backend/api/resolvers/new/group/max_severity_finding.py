# Standard
from typing import cast, List, Optional

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from graphql.language.ast import SelectionSetNode
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.api.resolvers import finding as old_resolver
from backend.decorators import get_entity_cache_async, require_integrates
from backend.typing import Finding, Project as Group


@require_integrates
@get_entity_cache_async
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Optional[Finding]:
    group_name: str = cast(str, parent['name'])

    group_findings_loader: DataLoader = info.context.loaders['group_findings']
    finding_ids: List[str] = [
        finding['id']
        for finding in await group_findings_loader.load(group_name)
    ]

    finding_loader: DataLoader = info.context.loaders['finding']
    findings = await finding_loader.load_many(finding_ids)

    _, max_severity_finding_id = max([
        (finding['severity_score'], finding['id'])
        for finding in findings
    ]) if findings else (0, '')

    # Temporary while migrating finding resolvers
    if max_severity_finding_id:
        finding = await old_resolver.resolve(
            info,
            max_severity_finding_id,
            as_field=True,
            selection_set=cast(
                SelectionSetNode,
                info.field_nodes[0].selection_set
            )
        )
        return cast(
            Finding, dict(zip(finding, await collect(finding.values())))
        )

    return None
