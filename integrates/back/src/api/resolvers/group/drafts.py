from aiodataloader import (
    DataLoader,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
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
    Any,
    Dict,
    Tuple,
    Union,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[Finding, ...]:
    group_drafts_loader: DataLoader = info.context.loaders.group_drafts
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    drafts: Tuple[Finding, ...] = await group_drafts_loader.load(group_name)
    return drafts
