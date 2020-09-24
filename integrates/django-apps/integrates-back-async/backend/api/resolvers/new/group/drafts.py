# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.typing import Finding, Project as Group


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Finding]:
    group_name: str = cast(str, parent['name'])

    group_loader: DataLoader = info.context.loaders['project']
    draft_ids: List[str] = (await group_loader.load(group_name))['drafts']

    finding_loader: DataLoader = info.context.loaders['finding']
    drafts: List[Finding] = await finding_loader.load_many(draft_ids)

    return drafts
