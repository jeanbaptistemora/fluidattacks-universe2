# Standard
from typing import cast

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
) -> int:
    group_name: str = cast(str, parent['name'])
    group_findings_loader: DataLoader = info.context.loaders['group_findings']

    return len(await group_findings_loader.load(group_name))
