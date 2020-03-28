# pylint: disable=import-error

import rollbar

from backend.decorators import (
    enforce_group_level_auth_async, require_login, require_project_access,
    enforce_user_level_auth_async,
)
from backend.domain import (
    project as project_domain,
    user as user_domain,
)
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
def resolve_create_project(_, info, **kwargs):
    """Resolve create_project mutation."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = user_domain.get_user_level_role(user_email)
    success = project_domain.create_project(
        user_data['user_email'], user_role, **kwargs)
    if success:
        project = kwargs.get('project_name').lower()
        util.invalidate_cache(user_data['user_email'])
        util.cloudwatch_log(
            info.context,
            f'Security: Created project {project} successfully')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_request_remove_project(_, info, project_name):
    """Resolve request_remove_project mutation."""
    user_info = util.get_jwt_content(info.context)
    success = \
        project_domain.request_deletion(project_name, user_info['user_email'])
    if success:
        project = project_name.lower()
        util.invalidate_cache(project)
        util.cloudwatch_log(
            info.context,
            f'Security: Pending to remove project {project}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_reject_remove_project(_, info, project_name):
    """Resolve reject_remove_project mutation."""
    user_info = util.get_jwt_content(info.context)
    success = \
        project_domain.reject_deletion(project_name, user_info['user_email'])
    if success:
        project = project_name.lower()
        util.invalidate_cache(project)
        util.cloudwatch_log(
            info.context,
            f'Security: Reject project {project} deletion succesfully')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_add_tags(_, info, project_name, tags):
    """Resolve add_tags mutation."""
    success = False
    project_name = project_name.lower()
    if project_domain.is_alive(project_name):
        if project_domain.validate_tags(project_name, tags):
            project_tags = project_domain.get_attributes(project_name, ['tag'])
            if not project_tags:
                project_tags = {'tag': set(tag for tag in tags)}
            else:
                project_tags.get('tag').update(tags)
            tags_added = project_domain.update(project_name, project_tags)
            if tags_added:
                success = True
            else:
                rollbar.report_message('Error: \
An error occurred adding tags', 'error', info.context)
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to upload tags without the allowed structure')
    else:
        util.cloudwatch_log(info.context,
                            'Security: \
Attempted to upload tags without the allowed validations')
    if success:
        util.invalidate_cache(project_name)
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_remove_tag(_, info, project_name, tag):
    """Resolve remove_tag mutation."""
    success = False
    project_name = project_name.lower()
    if project_domain.is_alive(project_name):
        project_tags = project_domain.get_attributes(project_name, ['tag'])
        project_tags.get('tag').remove(tag)
        if project_tags.get('tag') == set():
            project_tags['tag'] = None
        tag_deleted = project_domain.update(project_name, project_tags)
        if tag_deleted:
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred removing a tag', 'error', info.context)
    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(info.context, 'Security: Removed tag from \
            {project} project succesfully'.format(project=project_name))
    else:
        util.cloudwatch_log(info.context, 'Security: Attempted to remove \
            tag in {project} project'.format(project=project_name))
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
def resolve_add_all_project_access(_, info, project_name):
    """Resolve add_all_project_access mutation."""
    success = project_domain.add_all_access_to_project(project_name)
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Add all project access of {project_name}')
        util.invalidate_cache(project_name)
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
def resolve_remove_all_project_access(_, info, project_name):
    """Resolve remove_all_project_access mutation."""
    success = project_domain.remove_all_project_access(project_name)
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Remove all project access of {project_name}')
        util.invalidate_cache(project_name)
    return dict(success=success)
