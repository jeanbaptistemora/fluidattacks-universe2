from datetime import datetime
from time import time
import sys

from typing import List
from asgiref.sync import sync_to_async

from backend.api.dataloaders.event import EventLoader
from backend.decorators import (
    get_entity_cache_async, require_login, require_event_access, rename_kwargs,
    require_integrates,
    require_project_access, enforce_group_level_auth_async
)
from backend.domain import comment as comment_domain
from backend.domain import event as event_domain
from backend.domain import project as project_domain
from backend.typing import (
    Event as EventType,
    Historic as HistoricType,
    Comment as CommentType,
    SimplePayload as SimplePayloadType,
    AddCommentPayload as AddCommentPayloadType,
    DownloadFilePayload as DownloadFilePayloadType,
)
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@get_entity_cache_async
async def _get_id(_, identifier: str) -> str:
    """Get bts_url."""
    return identifier


@get_entity_cache_async
async def _get_analyst(info, identifier: str) -> str:
    """Get analyst."""
    event = await info.context.loaders['event'].load(identifier)
    return event['analyst']


@get_entity_cache_async
async def _get_client(info, identifier: str) -> str:
    """Get client."""
    event = await info.context.loaders['event'].load(identifier)
    return event['client']


@get_entity_cache_async
async def _get_evidence(info, identifier: str) -> str:
    """Get evidence."""
    event = await info.context.loaders['event'].load(identifier)
    return event['evidence']


@get_entity_cache_async
async def _get_project_name(info, identifier: str) -> str:
    """Get project_name."""
    event = await info.context.loaders['event'].load(identifier)
    return event['project_name']


@get_entity_cache_async
async def _get_client_project(info, identifier: str) -> str:
    """Get client_project."""
    event = await info.context.loaders['event'].load(identifier)
    return event['client_project']


@get_entity_cache_async
async def _get_event_type(info, identifier: str) -> str:
    """Get event_type."""
    event = await info.context.loaders['event'].load(identifier)
    return event['event_type']


@get_entity_cache_async
async def _get_detail(info, identifier: str) -> str:
    """Get detail."""
    event = await info.context.loaders['event'].load(identifier)
    return event['detail']


@get_entity_cache_async
async def _get_event_date(info, identifier: str) -> str:
    """Get event_date."""
    event = await info.context.loaders['event'].load(identifier)
    return event['event_date']


@get_entity_cache_async
async def _get_event_status(info, identifier: str) -> str:
    """Get event_status."""
    event = await info.context.loaders['event'].load(identifier)
    return event['event_status']


@get_entity_cache_async
async def _get_historic_state(info,
                              identifier: str) -> HistoricType:
    """Get historic_state."""
    event = await info.context.loaders['event'].load(identifier)
    return event['historic_state']


@get_entity_cache_async
async def _get_affectation(info, identifier: str) -> str:
    """Get affectation."""
    event = await info.context.loaders['event'].load(identifier)
    return event['affectation']


@get_entity_cache_async
async def _get_accessibility(info, identifier: str) -> str:
    """Get accessibility."""
    event = await info.context.loaders['event'].load(identifier)
    return event['accessibility']


@get_entity_cache_async
async def _get_affected_components(info, identifier: str) -> str:
    """Get affected_components."""
    event = await info.context.loaders['event'].load(identifier)
    return event['affected_components']


@get_entity_cache_async
async def _get_context(info, identifier: str) -> str:
    """Get context."""
    event = await info.context.loaders['event'].load(identifier)
    return event['context']


@get_entity_cache_async
async def _get_subscription(info, identifier: str) -> str:
    """Get subscription."""
    event = await info.context.loaders['event'].load(identifier)
    return event['subscription']


@get_entity_cache_async
async def _get_evidence_file(info, identifier: str) -> str:
    """Get evidence_file."""
    event = await info.context.loaders['event'].load(identifier)
    return event['evidence_file']


@get_entity_cache_async
async def _get_closing_date(info, identifier: str) -> str:
    """Get closing_date."""
    event = await info.context.loaders['event'].load(identifier)
    return event['closing_date']


@get_entity_cache_async
async def _get_comments(info, identifier: str) -> List[CommentType]:
    """Get comments."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    event = await info.context.loaders['event'].load(identifier)
    project_name = event['project_name']

    comments = await comment_domain.get_event_comments(
        project_name, identifier, user_email)
    return comments


@convert_kwargs_to_snake_case
async def resolve_event_mutation(obj, info, **parameters):
    """Resolve update_severity mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


async def resolve(info, identifier: str = '',
                  as_field: bool = False) -> EventType:
    """Async resolve fields."""
    result: EventType = dict()
    requested_fields = \
        util.get_requested_fields('findings',
                                  info.field_nodes[0].selection_set) \
        if as_field else info.field_nodes[0].selection_set.selections

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'identifier': identifier
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


@require_login
@rename_kwargs({'identifier': 'event_id'})
@enforce_group_level_auth_async
@require_integrates
@require_event_access
@rename_kwargs({'event_id': 'identifier'})
@convert_kwargs_to_snake_case
async def resolve_event(_, info, identifier: str = '') -> EventType:
    """Resolve event query."""
    return await resolve(info, identifier)


@get_entity_cache_async
async def _resolve_events_async(event_ids: List[str]) -> List[EventType]:
    """Async resolve events function."""
    return await EventLoader().load_many(event_ids)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_integrates
@require_project_access
async def resolve_events(_, info, project_name: str) -> List[EventType]:
    """Resolve events query."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} events')  # pragma: no cover
    event_ids = project_domain.list_events(project_name)
    return await _resolve_events_async(event_ids)


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_project_access
async def _do_create_event(_, info, project_name: str, image=None, file=None,
                           **kwa) -> SimplePayloadType:
    """Resolve create_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = await event_domain.create_event(
        analyst_email, project_name.lower(), file, image, **kwa)
    if success:
        util.cloudwatch_log(
            info.context, 'Security: Created event in '
            f'{project_name} project successfully')  # pragma: no cover
        util.invalidate_cache(project_name)
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_event_access
async def _do_solve_event(_, info, event_id: str, affectation: str,
                          date: datetime) -> SimplePayloadType:
    """Resolve solve_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = await event_domain.solve_event(
        event_id, affectation, analyst_email, date)
    if success:
        event = await event_domain.get_event(event_id)
        project_name = str(event.get('project_name', ''))
        util.invalidate_cache(event_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Solved event {event_id} '
            'successfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to '
            f'solve event {event_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_event_access
async def _do_add_event_comment(_, info, content: str, event_id: str,
                                parent: str) -> AddCommentPayloadType:
    """Resolve add_event_comment mutation."""
    random_comment_id = int(round(time() * 1000))
    user_info = util.get_jwt_content(info.context)
    comment_id, success = await \
        event_domain.add_comment(
            random_comment_id, content, event_id, parent, user_info)
    if success:
        util.invalidate_cache(event_id)
        util.cloudwatch_log(
            info.context,
            'Security: Added comment to '
            f'event {event_id} successfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to add comment '
            f'in event {event_id}')  # pragma: no cover
    return AddCommentPayloadType(success=success, comment_id=str(comment_id))


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_event_access
async def _do_update_event_evidence(_, info, event_id: str, evidence_type: str,
                                    file) -> SimplePayloadType:
    """Resolve update_event_evidence mutation."""
    success = False
    if await \
            sync_to_async(event_domain.validate_evidence)(evidence_type, file):
        success = await event_domain.update_evidence(
            event_id, evidence_type, file)
    if success:
        util.invalidate_cache(event_id)
        util.cloudwatch_log(
            info.context,
            'Security: Updated evidence in '
            f'event {event_id} successfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to update evidence '
            f'in event {event_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_event_access
async def _do_download_event_file(_, info, event_id: str,
                                  file_name: str) -> DownloadFilePayloadType:
    """Resolve download_event_file mutation."""
    success = False
    signed_url = await \
        sync_to_async(event_domain.get_evidence_link)(event_id, file_name)
    if signed_url:
        util.cloudwatch_log(
            info.context,
            'Security: Downloaded file in event '
            f'{event_id} successfully')  # pragma: no cover
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to download '
            f'file in event {event_id}')  # pragma: no cover
    return DownloadFilePayloadType(success=success, url=signed_url)


@require_login
@enforce_group_level_auth_async
@require_integrates
@require_event_access
async def _do_remove_event_evidence(_, info, event_id: str,
                                    evidence_type: str) -> SimplePayloadType:
    """Resolve remove_event_evidence mutation."""
    success = await event_domain.remove_evidence(evidence_type, event_id)
    if success:
        util.cloudwatch_log(
            info.context,
            'Security: Removed evidence in '
            f'event {event_id}')  # pragma: no cover
        util.invalidate_cache(event_id)
    return SimplePayloadType(success=success)
