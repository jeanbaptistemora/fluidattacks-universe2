# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from model.findings.types import Finding


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Finding:
    finding_id: str = kwargs['finding_id']
    group_name: str = kwargs['group_name']
    finding_loader: DataLoader = info.context.loaders.finding_new
    finding: Finding = await finding_loader.load((group_name, finding_id))

    return finding
