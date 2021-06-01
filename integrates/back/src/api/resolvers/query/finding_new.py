from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def _get_draft(finding: Finding, _info: GraphQLResolveInfo) -> Finding:
    return finding


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_integrates
)
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Finding:
    finding_id: str = kwargs["identifier"]
    group_name: str = kwargs["group_name"]
    finding_loader: DataLoader = info.context.loaders.finding_new
    finding: Finding = await finding_loader.load((group_name, finding_id))
    if finding.approval is None:
        return await _get_draft(finding, info)

    return finding
