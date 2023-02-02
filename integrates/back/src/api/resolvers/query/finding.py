from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@enforce_group_level_auth_async
async def _get_draft(finding: Finding, **_kwargs: Any) -> Finding:
    return finding


@convert_kwargs_to_snake_case
@rename_kwargs({"identifier": "finding_id"})
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Finding:
    finding_id: str = kwargs["finding_id"]
    loaders: Dataloaders = info.context.loaders
    finding = await findings_domain.get_finding(loaders, finding_id)
    if finding.approval is None:
        return await _get_draft(finding, info=info)

    return finding
