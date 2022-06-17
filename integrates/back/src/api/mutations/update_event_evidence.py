from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.events.enums import (
    EventEvidenceType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_now,
)
from starlette.datastructures import (
    UploadFile,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str,
    file: UploadFile,
) -> SimplePayload:
    success = False
    evidence_type_enum = EventEvidenceType[evidence_type]
    await events_domain.validate_evidence(evidence_type_enum, file)

    success = await events_domain.update_evidence(
        event_id,
        evidence_type_enum,
        file,
        get_now(),
    )
    info.context.loaders.event.clear(event_id)

    return SimplePayload(success=success)
