# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql.type.definition import GraphQLResolveInfo

# Local
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
    file: InMemoryUploadedFile
) -> SimplePayload:
    success = False
    if await event_domain.validate_evidence(evidence_type, file):
        success = await event_domain.update_evidence(
            event_id,
            evidence_type,
            file
        )

    return SimplePayload(success=success)
