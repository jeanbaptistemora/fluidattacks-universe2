# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from events import domain as events_domain
from newutils import logs as logs_utils


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str
) -> SimplePayload:
    """Resolve remove_event_evidence mutation."""
    success = await events_domain.remove_evidence(evidence_type, event_id)
    if success:
        info.context.loaders.event.clear(event_id)
        logs_utils.cloudwatch_log(
            info.context,
            f'Security: Removed evidence in event {event_id}'
        )
    return SimplePayload(success=success)
