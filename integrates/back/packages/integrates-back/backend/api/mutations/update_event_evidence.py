# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.domain import event as event_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    _info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str,
    file: UploadFile
) -> SimplePayload:
    success = False
    if await event_domain.validate_evidence(evidence_type, file):
        success = await event_domain.update_evidence(
            event_id,
            evidence_type,
            file
        )
        await util.invalidate_cache(f'view*events*{event_id}')

    return SimplePayload(success=success)
