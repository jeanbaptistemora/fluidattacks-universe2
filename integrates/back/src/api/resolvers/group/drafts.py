from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    List,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Finding]:
    group_drafts_loader: DataLoader = info.context.loaders.group_drafts
    finding_loader: DataLoader = info.context.loaders.finding

    group_name: str = cast(str, parent["name"])
    draft_ids: List[str] = [
        finding["id"] for finding in await group_drafts_loader.load(group_name)
    ]
    drafts: List[Finding] = await finding_loader.load_many(draft_ids)
    return drafts
