from datetime import datetime
from time import time
import sys
from typing import Any, Union, cast

from ariadne import convert_kwargs_to_snake_case
from django.core.files.uploadedfile import InMemoryUploadedFile

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
async def _do_create_event(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        image: Union[InMemoryUploadedFile, None] = None,
        file: Union[InMemoryUploadedFile, None] = None,
        **kwa: Any) -> SimplePayloadType:
    """Resolve create_event mutation."""
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await event_domain.create_event(
        analyst_email, project_name.lower(), file, image, **kwa
    )
    if success:
        util.cloudwatch_log(
            info.context,
            ('Security: Created event in '
             f'{project_name} project successfully')  # pragma: no cover
        )
        util.queue_cache_invalidation(project_name)
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_solve_event(
        _: Any,
        info: GraphQLResolveInfo,
        event_id: str,
        affectation: str,
        date: datetime) -> SimplePayloadType:
    """Resolve solve_event mutation."""
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await event_domain.solve_event(
        event_id, affectation, analyst_email, date
    )
    if success:
        event = await event_domain.get_event(event_id)
        project_name = str(event.get('project_name', ''))
        util.queue_cache_invalidation(event_id, project_name)
        util.cloudwatch_log(
            info.context,
            (f'Security: Solved event {event_id} '
             'successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to '
             f'solve event {event_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_event_consult(
        _: Any,
        info: GraphQLResolveInfo,
        content: str,
        event_id: str,
        parent: str) -> AddConsultPayloadType:
    random_comment_id = int(round(time() * 1000))
    user_info: Any = await util.get_jwt_content(info.context)
    user_email = str(user_info['user_email'])
    comment_data = {
        'comment_type': 'event',
        'parent': parent,
        'content': content,
        'user_id': random_comment_id
    }
    comment_id, success = await event_domain.add_comment(
        user_email,
        comment_data,
        event_id,
        parent
    )
    if success:
        util.queue_cache_invalidation(
            f'consulting*{event_id}',
            f'comment*{event_id}'
        )
        event_domain.send_comment_mail(
            user_email,
            comment_data,
            await info.context.loaders['event'].load(event_id)
        )
        util.cloudwatch_log(
            info.context,
            ('Security: Added comment to '
             f'event {event_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to add comment '
             f'in event {event_id}')  # pragma: no cover
        )
    return AddConsultPayloadType(success=success, comment_id=str(comment_id))


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_update_event_evidence(
        _: Any,
        info: GraphQLResolveInfo,
        event_id: str,
        evidence_type: str,
        file: InMemoryUploadedFile) -> SimplePayloadType:
    """Resolve update_event_evidence mutation."""
    success = False
    if await event_domain.validate_evidence(evidence_type, file):
        success = await event_domain.update_evidence(
            event_id, evidence_type, file)
    if success:
        util.queue_cache_invalidation(f'evidence*{event_id}')
        util.cloudwatch_log(
            info.context,
            ('Security: Updated evidence in '
             f'event {event_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update evidence '
             f'in event {event_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_download_event_file(
        _: Any,
        info: GraphQLResolveInfo,
        event_id: str,
        file_name: str) -> DownloadFilePayloadType:
    """Resolve download_event_file mutation."""
    success = False
    signed_url = await event_domain.get_evidence_link(event_id, file_name)
    if signed_url:
        util.cloudwatch_log(
            info.context,
            ('Security: Downloaded file in event '
             f'{event_id} successfully')  # pragma: no cover
        )
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to download '
             f'file in event {event_id}')  # pragma: no cover
        )
    return DownloadFilePayloadType(success=success, url=signed_url)


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
