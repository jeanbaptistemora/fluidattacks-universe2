from datetime import datetime
import sys
import time
from typing import Dict, List, Set, cast, Union
from graphql.language.ast import FieldNode, SelectionSetNode, ObjectFieldNode
import simplejson as json
from asgiref.sync import sync_to_async
import rollbar

from backend.api.resolvers import (
    finding as finding_loader,
    user as user_loader
)

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, require_login,
    require_project_access, enforce_user_level_auth_async
)
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    user as user_domain
)
from backend.typing import (
    Comment as CommentType,
    Event as EventType,
    Finding as FindingType,
    Project as ProjectType,
    User as UserType,
    AddCommentPayload as AddCommentPayloadType,
    SimplePayload as SimplePayloadType,
    SimpleProjectPayload as SimpleProjectPayloadType,
)
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


async def __get_filtered_findings(findings, filters):
    """Return filtered findings accorging to filters."""
    # This should be called with all() in the future, but there's a known bug
    # of Python that currently prevents it: https://bugs.python.org/issue39562
    filtered = []
    if filters:
        for finding in findings:
            hit_counter = 0
            len_filters = len(filters)
            for filt in filters:
                filt_key = util.camelcase_to_snakecase(filt.name.value)
                coro_result = await finding[filt_key]
                if str(coro_result) == str(filt.value.value):
                    hit_counter += 1
            if hit_counter == len_filters:
                filtered.append(finding)
    return filtered


@sync_to_async
def _get_name(_, project_name: str, **__) -> str:
    """Get name."""
    return project_name


@get_entity_cache_async
async def _get_remediated_over_time(info, project_name: str,
                                    **__) -> str:
    """Get remediated_over_time."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    remediate_over_time_decimal = project_attrs.get('remediated_over_time', {})
    remediated_twelve_weeks = \
        [lst_rem[-12:] for lst_rem in remediate_over_time_decimal]
    remediated_over_time = json.dumps(
        remediated_twelve_weeks, use_decimal=True)
    return remediated_over_time


@get_entity_cache_async
async def _get_has_drills(info, project_name: str, **__) -> Dict[str, bool]:
    """Get has_drills."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('has_drills', False)


@get_entity_cache_async
async def _get_has_forces(info, project_name: str, **__) -> Dict[str, bool]:
    """Get has_forces."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('has_forces', False)


async def _get_findings(
        info, project_name: str, requested_fields: list,
        filters=None) -> Dict[str, List[Dict[str, FindingType]]]:
    """Resolve findings attribute."""
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    req_fields.extend(util.get_requested_fields('findings', selection_set))
    if filters:
        req_fields.extend(filters)
    selection_set.selections = req_fields
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} findings')  # pragma: no cover
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = \
        await info.context.loaders['finding'].load_many(project_findings)

    findings = [
        await finding_loader.resolve(info, finding['id'], as_field=True,
                                     selection_set=selection_set)
        for finding in findings
        if 'current_state' in finding and finding['current_state'] != 'DELETED'
    ]
    filtered = await __get_filtered_findings(findings, filters)
    return filtered if filters else findings


@get_entity_cache_async
async def _get_open_vulnerabilities(info, project_name: str,
                                    **__) -> int:
    """Get open_vulnerabilities."""
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(project_findings)

    # This should be a list comprehension in the future, but there's a known
    # bug of Python that prevents it: https://bugs.python.org/issue39562
    open_vulnerabilities = 0
    for vulns in finding_vulns:
        for vuln in vulns:
            if 'current_state' in vuln and \
                vuln['current_state'] == 'open' and \
                (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status']):
                open_vulnerabilities += 1
    return open_vulnerabilities


@get_entity_cache_async
async def _get_open_findings(info,
                             project_name: str, **__) -> int:
    """Get open_findings."""
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(project_findings)
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(finding_ids)
    open_findings = \
        await sync_to_async(project_domain.get_open_findings)(finding_vulns)
    return open_findings


@get_entity_cache_async
async def _get_closed_vulnerabilities(
        info, project_name: str, **__) -> int:
    """Get closed_vulnerabilities."""
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(project_findings)

    # This should be a list comprehension in the future, but there's a known
    # bug of Python that prevents it: https://bugs.python.org/issue39562
    closed_vulnerabilities = 0
    for vulns in finding_vulns:
        for vuln in vulns:
            if 'current_state' in vuln and \
                vuln['current_state'] == 'closed' and \
                (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status']):
                closed_vulnerabilities += 1
    return closed_vulnerabilities


@get_entity_cache_async
async def _get_pending_closing_check(_, project_name: str,
                                     **__) -> int:
    """Get pending_closing_check."""
    pending_closing_check = await \
        sync_to_async(project_domain.get_pending_closing_check)(project_name)
    return pending_closing_check


@get_entity_cache_async
async def _get_last_closing_vuln(info, project_name: str, **__) -> int:
    """Get last_closing_vuln."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    last_closing_vuln = project_attrs.get('last_closing_date', 0)
    return last_closing_vuln


@get_entity_cache_async
async def _get_max_severity(info, project_name: str, **__) -> float:
    """Get max_severity."""
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = \
        await info.context.loaders['finding'].load_many(project_findings)

    max_severity = max(
        [finding['severity_score'] for finding in findings
         if 'current_state' in finding and
         finding['current_state'] != 'DELETED']) if findings else 0
    return max_severity


@get_entity_cache_async
async def _get_max_open_severity(info, project_name: str,
                                 **__) -> float:
    """Resolve maximum severity in open vulnerability attribute."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('max_open_severity', 0)


@get_entity_cache_async
async def _get_mean_remediate(info, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('mean_remediate', 0)


@get_entity_cache_async
async def _get_mean_remediate_low_severity(
        info, project_name: str, **__) -> int:
    """Get mean_remediate_low_severity."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('mean_remediate_low_severity', 0)


@get_entity_cache_async
async def _get_mean_remediate_medium_severity(
        info, project_name: str, **__) -> int:
    """Get mean_remediate_medium_severity."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('mean_remediate_medium_severity', 0)


@get_entity_cache_async
async def _get_mean_remediate_high_severity(
        info, project_name: str, **__) -> int:
    """Get mean_remediate_high_severity."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('mean_remediate_high_severity', 0)


@get_entity_cache_async
async def _get_mean_remediate_critical_severity(
        info, project_name: str, **__) -> int:
    """Get mean_remediate_critical_severity."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('mean_remediate_critical_severity', 0)


@get_entity_cache_async
async def _get_total_findings(info, project_name: str, **__) -> int:
    """Get total_findings."""
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = \
        await info.context.loaders['finding'].load_many(project_findings)

    total_findings = sum(1 for finding in findings
                         if 'current_state' in finding and
                         finding['current_state'] != 'DELETED')
    return total_findings


@get_entity_cache_async
async def _get_total_treatment(info, project_name: str, **__) -> str:
    """Get total_treatment."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    total_treatment_decimal = project_attrs.get('total_treatment', {})
    total_treatment = json.dumps(
        total_treatment_decimal, use_decimal=True)
    return total_treatment


@get_entity_cache_async
async def _get_current_month_authors(_, project_name: str,
                                     **__) -> Dict[str, int]:
    """Get current_month_authors."""
    current_month_authors = await \
        sync_to_async(project_domain.get_current_month_authors)(
            project_name
        )
    return current_month_authors


@get_entity_cache_async
async def _get_current_month_commits(_, project_name: str,
                                     **__) -> Dict[str, int]:
    """Get current_month_commits."""
    current_month_commits = await \
        sync_to_async(project_domain.get_current_month_commits)(
            project_name
        )
    return current_month_commits


@get_entity_cache_async
async def _get_subscription(info, project_name: str, **__) -> Dict[str, str]:
    """Get subscription."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('type', '')


@get_entity_cache_async
async def _get_deletion_date(_, project_name: str, **__) -> Dict[str, str]:
    """Get deletion_date."""
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    deletion_date = \
        historic_deletion[-1].get('deletion_date', '') \
        if historic_deletion else ''
    return deletion_date


@get_entity_cache_async
async def _get_user_deletion(_, project_name: str, **__) -> str:
    """Get user_deletion."""
    user_deletion = ''
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    if historic_deletion and historic_deletion[-1].get('deletion_date'):
        user_deletion = historic_deletion[-1].get('user', '')
    return user_deletion


@get_entity_cache_async
async def _get_tags(info, project_name: str, **__) -> Dict[str, List[str]]:
    """Get tags."""
    project_attrs = \
        await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return project_attrs.get('tag', [])


@get_entity_cache_async
async def _get_description(_, project_name: str, **__) -> Dict[str, str]:
    """Get description."""
    return await \
        sync_to_async(project_domain.get_description)(project_name)


@enforce_group_level_auth_async
async def _get_comments(
        info, project_name: str, **__) -> Dict[str, List[CommentType]]:
    """Get comments."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    comments = await sync_to_async(project_domain.list_comments)(
        project_name, user_email)
    return comments


@enforce_group_level_auth_async
async def _get_drafts(
        info, project_name: str, **__) -> \
        List[Dict[str, FindingType]]:
    """Get drafts."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} drafts')  # pragma: no cover
    project_drafts = \
        await info.context.loaders['project'].load(project_name)
    project_drafts = project_drafts['drafts']
    drafts_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(project_drafts)
    findings = \
        await info.context.loaders['finding'].load_many(drafts_ids)

    drafts = [draft for draft in findings
              if 'current_state' in draft and
              draft['current_state'] != 'DELETED']
    return drafts


@enforce_group_level_auth_async
async def _get_events(info,
                      project_name: str, **__) -> Dict[str, List[EventType]]:
    """Get events."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} events')  # pragma: no cover
    event_ids = await \
        sync_to_async(project_domain.list_events)(project_name)
    events = \
        await info.context.loaders['event'].load_many(event_ids)
    return events


@enforce_group_level_auth_async
async def _get_users(info, project_name: str,
                     requested_fields: list) -> List[UserType]:
    """Get users."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = await \
        sync_to_async(user_domain.get_group_level_role)(
            user_email, project_name
        )

    init_email_list = await \
        sync_to_async(project_domain.get_users)(project_name)
    user_email_list = util.user_email_filter(
        init_email_list, user_email)
    user_roles_to_retrieve = ['customer', 'customeradmin', 'internal_manager']
    if user_role == 'admin':
        user_roles_to_retrieve.append('admin')
        user_roles_to_retrieve.append('analyst')
    as_field = True
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    users = [
        await user_loader.resolve(info, email, project_name,
                                  as_field, selection_set)
        for email in user_email_list
        if user_domain.get_group_level_role(email, project_name)
        in user_roles_to_retrieve]
    return users


async def resolve(info, project_name: str,
                  as_field: bool = False, as_list: bool = True) -> ProjectType:
    """Async resolve fields."""
    project_name = project_name.lower()
    result: ProjectType = dict()

    if as_field and as_list:
        requested_fields = util.get_requested_fields(
            'projects', info.field_nodes[0].selection_set)
    elif as_field:
        requested_fields = util.get_requested_fields(
            'project', info.field_nodes[0].selection_set)
    else:
        requested_fields = info.field_nodes[0].selection_set.selections

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'project_name': project_name,
            'requested_fields': requested_fields
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


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
async def resolve_project(_, info, project_name: str) -> ProjectType:
    """Resolve project query."""
    return await resolve(info, project_name)


@convert_kwargs_to_snake_case
async def resolve_project_mutation(obj, info, **parameters):
    """Wrap project mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


@require_login
@enforce_user_level_auth_async
async def _do_create_project(_, info, **kwargs) -> SimplePayloadType:
    """Resolve create_project mutation."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = \
        await sync_to_async(user_domain.get_user_level_role)(user_email)
    success = await sync_to_async(project_domain.create_project)(
        user_data['user_email'], user_role, **kwargs)
    if success:
        project = kwargs.get('project_name', '').lower()
        util.invalidate_cache(user_data['user_email'])
        util.cloudwatch_log(
            info.context,
            f'Security: Created project {project} '
            'successfully')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_request_remove_project(
        _, info, project_name: str) -> SimplePayloadType:
    """Resolve request_remove_project mutation."""
    user_info = util.get_jwt_content(info.context)
    success = \
        await sync_to_async(project_domain.request_deletion)(
            project_name, user_info['user_email'])
    if success:
        project = project_name.lower()
        util.invalidate_cache(project)
        util.cloudwatch_log(
            info.context,
            'Security: '
            f'Pending to remove project {project}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_reject_remove_project(_, info,
                                    project_name: str) -> SimplePayloadType:
    """Resolve reject_remove_project mutation."""
    user_info = util.get_jwt_content(info.context)
    success = \
        await sync_to_async(project_domain.reject_deletion)(
            project_name, user_info['user_email'])
    if success:
        project = project_name.lower()
        util.invalidate_cache(project)
        util.cloudwatch_log(
            info.context,
            'Security: Reject project '
            f'{project} deletion succesfully')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_add_project_comment(_, info,
                                  **parameters) -> AddCommentPayloadType:
    """Resolve add_project_comment mutation."""
    project_name = parameters.get('project_name', '').lower()
    user_info = util.get_jwt_content(info.context)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_id = int(round(time.time() * 1000))
    comment_data = {
        'user_id': comment_id,
        'content': parameters.get('content'),
        'created': current_time,
        'fullname':
            str.join(' ', [user_info['first_name'],
                           user_info['last_name']]),
        'modified': current_time,
        'parent': parameters.get('parent')
    }
    success = await sync_to_async(project_domain.add_comment)(
        project_name, user_info['user_email'], comment_data)
    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context, 'Security: Added comment to '
            f'{project_name} project succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, 'Security: Attempted to add '
            f'comment in {project_name} project')  # pragma: no cover
    ret = AddCommentPayloadType(success=success, comment_id=str(comment_id))
    return ret


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_add_tags(_, info, project_name: str,
                       tags: List[str]) -> SimpleProjectPayloadType:
    """Resolve add_tags mutation."""
    success = False
    project_name = project_name.lower()
    if await sync_to_async(project_domain.is_alive)(project_name):
        if await sync_to_async(project_domain.validate_tags)(
                project_name, tags):
            project_attrs = \
                await info.context.loaders['project'].load(project_name)
            project_attrs = project_attrs['attrs']
            project_tags = cast(ProjectType, project_attrs.get('tag', {}))
            project_tags = {'tag': project_tags}
            if not project_tags:
                project_tags = {'tag': set(tags)}
            else:
                cast(Set[str], project_tags.get('tag')).update(tags)
            tags_added = \
                await sync_to_async(project_domain.update)(
                    project_name, project_tags)
            if tags_added:
                success = True
            else:
                await sync_to_async(rollbar.report_message)('Error: \
An error occurred adding tags', 'error', info.context)
        else:
            util.cloudwatch_log(
                info.context, 'Security: \
Attempted to upload tags without the allowed structure')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, 'Security: \
Attempted to upload tags without the allowed validations')  # pragma: no cover
    if success:
        util.invalidate_cache(project_name)
    project = await resolve(info, project_name, True, False)
    return SimpleProjectPayloadType(success=success, project=project)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_remove_tag(_, info, project_name: str,
                         tag: str) -> SimpleProjectPayloadType:
    """Resolve remove_tag mutation."""
    success = False
    project_name = project_name.lower()
    if await sync_to_async(project_domain.is_alive)(project_name):
        project_attrs = \
            await info.context.loaders['project'].load(project_name)
        project_attrs = project_attrs['attrs']
        project_tags = cast(ProjectType, project_attrs.get('tag', {}))
        project_tags = {'tag': project_tags}
        cast(Set[str], project_tags.get('tag')).remove(tag)
        if project_tags.get('tag') == set():
            project_tags['tag'] = None
        tag_deleted = \
            await sync_to_async(
                project_domain.update)(project_name, project_tags)
        if tag_deleted:
            success = True
        else:
            await sync_to_async(rollbar.report_message)('Error: \
An error occurred removing a tag', 'error', info.context)
    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context, 'Security: Removed tag from '
            f'{project_name} project succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, 'Security: Attempted to remove '
            f'tag in {project_name} project')  # pragma: no cover
    project = await resolve(info, project_name, True, False)
    return SimpleProjectPayloadType(success=success, project=project)


@require_login
@enforce_group_level_auth_async
async def _do_add_all_project_access(_, info,
                                     project_name: str) -> SimplePayloadType:
    """Resolve add_all_project_access mutation."""
    success = \
        await sync_to_async(project_domain.add_all_access_to_project)(
            project_name)
    if success:
        util.cloudwatch_log(
            info.context,
            'Security: '
            f'Add all project access of {project_name}')  # pragma: no cover
        util.invalidate_cache(project_name)
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
async def _do_remove_all_project_access(
        _, info, project_name: str) -> SimplePayloadType:
    """Resolve remove_all_project_access mutation."""
    success = \
        await sync_to_async(project_domain.remove_all_project_access)(
            project_name)
    if success:
        util.cloudwatch_log(
            info.context,
            'Security: Remove '
            f'all project access of {project_name}')  # pragma: no cover
        util.invalidate_cache(project_name)
    return SimplePayloadType(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
async def resolve_alive_projects(_, info) -> List[ProjectType]:
    """Resolve for ACTIVE and SUSPENDED projects."""
    return await _get_alive_projects(info)


async def _get_alive_projects(info) -> List[ProjectType]:
    """Resolve for ACTIVE and SUSPENDED projects."""
    alive_projects = await sync_to_async(project_domain.get_alive_projects)()
    return [await resolve(info, project) for project in alive_projects]
