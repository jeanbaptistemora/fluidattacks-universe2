from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from db_model.findings.types import (
    Finding,
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
    Tuple,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Finding, ...]:
    group_drafts_loader: DataLoader = info.context.loaders.group_drafts
    group_name: str = parent["name"]
    drafts: Tuple[Finding, ...] = await group_drafts_loader.load(group_name)
    return drafts
