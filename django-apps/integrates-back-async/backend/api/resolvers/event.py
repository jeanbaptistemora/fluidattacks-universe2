# pylint: disable=import-error

from backend.decorators import (
    get_cached, require_login, require_event_access,
    require_project_access, enforce_authz_async
)
from backend.domain import event as event_domain
from backend.domain import project as project_domain
from backend import util

from ariadne import convert_kwargs_to_snake_case


@require_login
@enforce_authz_async
@require_event_access
@get_cached
@convert_kwargs_to_snake_case
def resolve_event(_, info, identifier):
    """Resolve event query."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to Event: {identifier} succesfully')
    return event_domain.get_event(identifier)


@require_login
@enforce_authz_async
@require_event_access
@get_cached
@convert_kwargs_to_snake_case
def resolve_events(_, info, project_name):
    """Resolve events query."""
    util.cloudwatch_log(
        info.context, f'Security: Access to {project_name} events')
    event_ids = project_domain.list_events(project_name)
    events_loader = info.context.loaders['event']
    return events_loader.load_many(event_ids)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_update_event(_, info, event_id, **kwargs):
    """Resolve update_event mutation."""
    success = event_domain.update_event(event_id, **kwargs)
    if success:
        project_name = event_domain.get_event(event_id).get('project_name')
        util.invalidate_cache(event_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Updated event {event_id} succesfully')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_project_access
def resolve_create_event(_, info, project_name, image=None, file=None, **kwa):
    """Resolve create_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = event_domain.create_event(
        analyst_email, project_name.lower(), file, image, **kwa)
    if success:
        util.cloudwatch_log(info.context, 'Security: Created event in '
                            f'{project_name} project succesfully')
        util.invalidate_cache(project_name)
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_solve_event(_, info, event_id, affectation, date):
    """Resolve solve_event mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = event_domain.solve_event(
        event_id, affectation, analyst_email, date)
    if success:
        project_name = event_domain.get_event(event_id).get('project_name')
        util.invalidate_cache(event_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context, f'Security: Solved event {event_id} succesfully')
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to solve event {event_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_add_event_comment(_, info, content, event_id, parent):
    """Resolve add_event_comment mutation."""
    user_info = util.get_jwt_content(info.context)
    comment_id, success = event_domain.add_comment(
        content, event_id, parent, user_info)
    if success:
        util.invalidate_cache(event_id)
        util.cloudwatch_log(
            info.context,
            f'Security: Added comment to event {event_id} succesfully')
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add comment in event {event_id}')
    return dict(success=success, comment_id=comment_id)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_update_event_evidence(_, info, event_id, evidence_type, file):
    """Resolve update_event_evidence mutation."""
    success = False
    if event_domain.validate_evidence(evidence_type, file):
        success = event_domain.update_evidence(
            event_id, evidence_type, file)
    if success:
        util.invalidate_cache(event_id)
        util.cloudwatch_log(
            info.context,
            f'Security: Updated evidence in event {event_id} succesfully')
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to update evidence in event {event_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_download_event_file(_, info, event_id, file_name):
    """Resolve download_event_file mutation."""
    success = False
    signed_url = event_domain.get_evidence_link(event_id, file_name)
    if signed_url:
        util.cloudwatch_log(
            info.context,
            f'Security: Downloaded file in event {event_id} succesfully')
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to download file in event {event_id}')
    return dict(success=success, url=signed_url)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_event_access
def resolve_remove_event_evidence(_, info, event_id, evidence_type):
    """Resolve remove_event_evidence mutation."""
    success = event_domain.remove_evidence(evidence_type, event_id)
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Removed evidence in event {event_id}')
        util.invalidate_cache(event_id)
    return dict(success=success)
