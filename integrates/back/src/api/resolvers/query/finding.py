from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_integrates,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    findings as findings_utils,
)
from typing import (
    cast,
    Dict,
)


@enforce_group_level_auth_async
async def _get_draft(finding: Finding, _info: GraphQLResolveInfo) -> Finding:
    return finding


@convert_kwargs_to_snake_case
@rename_kwargs({"identifier": "finding_id"})
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_integrates
)
@rename_kwargs({"finding_id": "identifier"})
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Finding:
    finding_loader: DataLoader = info.context.loaders.finding
    finding_id: str = kwargs["identifier"]
    finding: Finding = await finding_loader.load(finding_id)

    is_draft = not findings_utils.is_released(
        cast(Dict[str, Finding], finding)
    )
    if is_draft:
        return await _get_draft(finding, info)
    return finding
