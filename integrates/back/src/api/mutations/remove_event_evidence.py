from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
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
from newutils import (
    logs as logs_utils,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, event_id: str, evidence_type: str
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    evidence_type_enum = EventEvidenceType[evidence_type]
    await events_domain.remove_evidence(loaders, evidence_type_enum, event_id)
    info.context.loaders.event_typed.clear(event_id)
    logs_utils.cloudwatch_log(
        info.context, f"Security: Removed evidence in event {event_id}"
    )

    return SimplePayload(success=True)
