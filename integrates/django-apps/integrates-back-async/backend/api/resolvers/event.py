import sys
from typing import Any, Union, cast

from ariadne import convert_kwargs_to_snake_case

from graphql.type.definition import GraphQLResolveInfo
from backend.decorators import (
    concurrent_decorators,
    require_login,
    require_integrates,
    enforce_group_level_auth_async
)
from backend.domain import event as event_domain
from backend.typing import (
    SimplePayload as SimplePayloadType,
    AddConsultPayload as AddConsultPayloadType,
    DownloadFilePayload as DownloadFilePayloadType,
)
from backend import util


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_event_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[SimplePayloadType, AddConsultPayloadType, DownloadFilePayloadType]:
    """Resolve update_severity mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[
            SimplePayloadType,
            AddConsultPayloadType,
            DownloadFilePayloadType
        ],
        await resolver_func(obj, info, **parameters)
    )


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_remove_event_evidence(
        _: Any,
        info: GraphQLResolveInfo,
        event_id: str,
        evidence_type: str) -> SimplePayloadType:
    """Resolve remove_event_evidence mutation."""
    success = await event_domain.remove_evidence(evidence_type, event_id)
    if success:
        util.queue_cache_invalidation(f'evidence*{event_id}')
        util.cloudwatch_log(
            info.context,
            ('Security: Removed evidence in '
             f'event {event_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
