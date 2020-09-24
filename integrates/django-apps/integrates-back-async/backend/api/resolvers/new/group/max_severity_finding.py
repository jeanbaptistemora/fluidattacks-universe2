# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async, require_integrates
from backend.typing import Finding, Project as Group


@require_integrates
@get_entity_cache_async
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Finding:
    group_name: str = cast(str, parent['name'])

    group_loader: DataLoader = info.context.loaders['project']
    finding_ids: List[str] = (await group_loader.load(group_name))['findings']

    finding_loader: DataLoader = info.context.loaders['finding']
    findings = await finding_loader.load_many(finding_ids)

    _, max_severity_finding_id = max([
        (finding['severity_score'], finding['id'])
        for finding in findings
    ]) if findings else (0, '')

    finding: Finding = await finding_loader.load(max_severity_finding_id)

    return finding
