# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async, require_integrates
from backend.typing import Project as Group


@require_integrates
@get_entity_cache_async
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> float:
    group_name: str = cast(str, parent['name'])

    group_loader: DataLoader = info.context.loaders['project']
    finding_ids: List[str] = (await group_loader.load(group_name))['findings']

    finding_loader: DataLoader = info.context.loaders['finding']
    findings = await finding_loader.load_many(finding_ids)

    max_severity: float = max([
        finding['severity_score']
        for finding in findings
    ]) if findings else 0

    return max_severity
