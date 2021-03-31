# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local
from backend.dal.helpers.redis import redis_del_by_deps
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import SimplePayload
from findings import domain as findings_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any
) -> SimplePayload:
    file: UploadFile = kwargs['file']
    finding_id: str = kwargs['finding_id']
    evidence_id: str = kwargs['evidence_id']

    success: bool = await findings_domain.validate_and_upload_evidence(
        finding_id,
        evidence_id,
        file
    )

    if success:
        info.context.loaders.finding.clear(finding_id)
        await redis_del_by_deps('update_evidence', finding_id=finding_id)

    return SimplePayload(success=success)
