# Standard
from typing import cast, Dict

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_integrates,
    require_login,
)
from backend.typing import Finding
from backend.filters import finding as finding_filters


@enforce_group_level_auth_async
async def _get_draft(finding: Finding, _info: GraphQLResolveInfo) -> Finding:
    return finding


@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
@rename_kwargs({'finding_id': 'identifier'})
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Finding:
    finding_id: str = kwargs['identifier']

    finding_loader: DataLoader = info.context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)

    is_draft = not finding_filters.is_released(
        cast(Dict[str, Finding], finding)
    )

    if is_draft:
        return await _get_draft(finding, info)

    return finding
