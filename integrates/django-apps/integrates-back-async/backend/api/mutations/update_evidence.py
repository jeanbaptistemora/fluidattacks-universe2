# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
async def mutate(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: Any
) -> SimplePayload:
    file: InMemoryUploadedFile = kwargs['file']
    finding_id: str = kwargs['finding_id']
    evidence_id: str = kwargs['evidence_id']

    success: bool = await finding_domain.validate_and_upload_evidence(
        finding_id,
        evidence_id,
        file
    )

    if success:
        if evidence_id == 'exploit':
            await util.invalidate_cache(f'exploit*{finding_id}')
        elif evidence_id == 'fileRecords':
            await util.invalidate_cache(f'records*{finding_id}')
        else:
            await util.invalidate_cache(f'evidence*{finding_id}')

    return SimplePayload(success=success)
