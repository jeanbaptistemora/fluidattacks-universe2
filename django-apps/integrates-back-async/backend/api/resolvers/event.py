# pylint: disable=import-error

from time import time
import sys

from asgiref.sync import sync_to_async

from backend.api.dataloaders.event import EventLoader
from backend.decorators import (
    get_cached, require_login, require_event_access, rename_kwargs,
    require_project_access, enforce_group_level_auth_async
)
from backend.domain import event as event_domain
from backend.domain import project as project_domain
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_event_mutation(obj, info, **parameters):
    """Resolve update_severity mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@require_login
@rename_kwargs({'identifier': 'event_id'})
@enforce_group_level_auth_async
@require_event_access
@rename_kwargs({'event_id': 'identifier'})
@get_cached
@convert_kwargs_to_snake_case
def resolve_event(_, info, identifier=None):
    """Resolve event query."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to Event: {identifier} succesfully')
    return event_domain.get_event(identifier)


async def _resolve_events_async(event_ids):
    """Async resolve events function."""
    return await EventLoader().load_many(event_ids)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_events(_, info, project_name):
    """Resolve events query."""
    util.cloudwatch_log(
        info.context, f'Security: Access to {project_name} events')
    event_ids = project_domain.list_events(project_name)
    return util.run_async(_resolve_events_async, event_ids)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_update_event(_, info, event_id, **kwargs):
    """Resolve update_event mutation."""
    success = await \
        sync_to_async(event_domain.update_event)(event_id, **kwargs)
    if success:
        event = await \
            sync_to_async(event_domain.get_event)(event_id)
        project_name = event.get('project_name')
        util.invalidate_cache(event_id)
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Updated event {event_id} succesfully')
    return dict(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_create_event(
    _, info, project_name, image=None, file=None, **kwa
):
    """Resolve create_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = await sync_to_async(event_domain.create_event)(
        analyst_email, project_name.lower(), file, image, **kwa)
    if success:
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Created event in '
            f'{project_name} project succesfully')
        util.invalidate_cache(project_name)
    return dict(success=success)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_solve_event(_, info, event_id, affectation, date):
    """Resolve solve_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = await sync_to_async(event_domain.solve_event)(
        event_id, affectation, analyst_email, date)
    if success:
        event = await \
            sync_to_async(event_domain.get_event)(event_id)
        project_name = event.get('project_name')
        util.invalidate_cache(event_id)
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Solved event {event_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to solve event {event_id}')
    return dict(success=success)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_add_event_comment(_, info, content, event_id, parent):
    """Resolve add_event_comment mutation."""
    comment_id = int(round(time() * 1000))
    user_info = util.get_jwt_content(info.context)
    comment_id, success = await \
        sync_to_async(event_domain.add_comment)(
            comment_id, content, event_id, parent, user_info)
    if success:
        util.invalidate_cache(event_id)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Added comment to event {event_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Attempted to add comment in event {event_id}')
    return dict(success=success, comment_id=comment_id)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_update_event_evidence(_, info, event_id, evidence_type, file):
    """Resolve update_event_evidence mutation."""
    success = False
    if await \
            sync_to_async(event_domain.validate_evidence)(evidence_type, file):
        success = await sync_to_async(event_domain.update_evidence)(
            event_id, evidence_type, file)
    if success:
        util.invalidate_cache(event_id)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Updated evidence in event {event_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Attempted to update evidence in event {event_id}')
    return dict(success=success)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_download_event_file(_, info, event_id, file_name):
    """Resolve download_event_file mutation."""
    success = False
    signed_url = await \
        sync_to_async(event_domain.get_evidence_link)(event_id, file_name)
    if signed_url:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Downloaded file in event {event_id} succesfully')
        success = True
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Attempted to download file in event {event_id}')
    return dict(success=success, url=signed_url)


@require_login
@enforce_group_level_auth_async
@require_event_access
async def _do_remove_event_evidence(_, info, event_id, evidence_type):
    """Resolve remove_event_evidence mutation."""
    success = await \
        sync_to_async(event_domain.remove_evidence)(evidence_type, event_id)
    if success:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Removed evidence in event {event_id}')
        util.invalidate_cache(event_id)
    return dict(success=success)
