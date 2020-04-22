# pylint: disable=import-error

from datetime import datetime
import asyncio
import sys
import time
from typing import Dict, List, Set, cast, Union
from graphql.language.ast import FieldNode, SelectionSetNode, ObjectFieldNode
import simplejson as json
from asgiref.sync import sync_to_async
import rollbar

from backend.api.dataloaders import (
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
    user as user_domain,
    vulnerability as vuln_domain
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


@sync_to_async
def _get_name(_, project_name: str, **__) -> Dict[str, str]:
    """Get name."""
    return dict(name=project_name)


@get_entity_cache_async
async def _get_remediated_over_time(_, project_name: str,
                                    **__) -> Dict[str, str]:
    """Get remediated_over_time."""
    remediated_over_time = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['remediated_over_time']
        )
    remediate_over_time_decimal = \
        remediated_over_time.get('remediated_over_time', {})
    remediated_twelve_weeks = \
        [lst_rem[-12:] for lst_rem in remediate_over_time_decimal]
    remediated_over_time = json.dumps(
        remediated_twelve_weeks, use_decimal=True)
    return dict(remediated_over_time=remediated_over_time)


@get_entity_cache_async
async def _get_has_drills(_, project_name: str, **__) -> Dict[str, bool]:
    """Get has_drills."""
    attributes = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['has_drills']
        )
    return dict(has_drills=attributes.get('has_drills', False))


@get_entity_cache_async
async def _get_has_forces(_, project_name: str, **__) -> Dict[str, bool]:
    """Get has_forces."""
    attributes = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['has_forces']
        )
    return dict(has_forces=attributes.get('has_forces', False))


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
    await sync_to_async(util.cloudwatch_log)(
        info.context,
        f'Security: Access to {project_name} findings')  # pragma: no cover
    finding_ids = await sync_to_async(finding_domain.filter_deleted_findings)(
        project_domain.list_findings(project_name)
    )
    findings = await info.context.loaders['finding'].load_many(finding_ids)
    as_field = True

    findings = [
        await finding_loader.resolve(info, finding['id'],
                                     as_field, selection_set)
        for finding in findings
        if finding['current_state'] != 'DELETED'
    ]
    if filters:
        findings = [
            finding for finding in findings
            if all(str(finding[util.camelcase_to_snakecase(filt.name.value)])
                   == str(filt.value.value) for filt in filters)
        ]
    return dict(findings=findings)


@get_entity_cache_async
async def _get_open_vulnerabilities(info, project_name: str,
                                    **__) -> Dict[str, int]:
    """Get open_vulnerabilities."""
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(
            project_domain.list_findings(project_name)
        )
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(finding_ids)

    # This should be async in the future, but there's a known bug of
    # Python that currently prevents it: https://bugs.python.org/issue39562
    open_vulnerabilities = sum([
        len([vuln for vuln in vulns
             if vuln_domain.get_current_state(vuln) == 'open'
             and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])])
        for vulns in finding_vulns
    ])
    return dict(open_vulnerabilities=open_vulnerabilities)


@get_entity_cache_async
async def _get_open_findings(info,
                             project_name: str, **__) -> Dict[str, int]:
    """Get open_findings."""
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(
            project_domain.list_findings(project_name)
        )
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(finding_ids)
    open_findings = \
        await sync_to_async(project_domain.get_open_findings)(finding_vulns)
    return dict(open_findings=open_findings)


@get_entity_cache_async
async def _get_closed_vulnerabilities(
        info, project_name: str, **__) -> Dict[str, int]:
    """Get closed_vulnerabilities."""
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(
            project_domain.list_findings(project_name)
        )
    finding_vulns = \
        await info.context.loaders['vulnerability'].load_many(finding_ids)

    # This should be async in the future, but there's a known bug of
    # Python that currently prevents it: https://bugs.python.org/issue39562
    closed_vulnerabilities = sum([
        len([vuln for vuln in vulns
             if vuln_domain.get_current_state(vuln) == 'closed'
             and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])])
        for vulns in finding_vulns
    ])
    return dict(closed_vulnerabilities=closed_vulnerabilities)


@get_entity_cache_async
async def _get_pending_closing_check(_, project_name: str,
                                     **__) -> Dict[str, int]:
    """Get pending_closing_check."""
    pending_closing_check = await \
        sync_to_async(project_domain.get_pending_closing_check)(project_name)
    return dict(pending_closing_check=pending_closing_check)


@get_entity_cache_async
async def _get_last_closing_vuln(_, project_name: str, **__) -> Dict[str, int]:
    """Get last_closing_vuln."""
    last_closing_vuln = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['last_closing_date']
        )
    last_closing_vuln = last_closing_vuln.get('last_closing_date', 0)
    return dict(last_closing_vuln=last_closing_vuln)


@get_entity_cache_async
async def _get_max_severity(info, project_name: str, **__) -> Dict[str, float]:
    """Get max_severity."""
    finding_ids = await sync_to_async(finding_domain.filter_deleted_findings)(
        project_domain.list_findings(project_name))
    findings = \
        await info.context.loaders['finding'].load_many(finding_ids)

    max_severity = max(
        [finding['severity_score'] for finding in findings
         if finding['current_state'] != 'DELETED']) if findings else 0
    return dict(max_severity=max_severity)


@get_entity_cache_async
async def _get_max_open_severity(_, project_name: str,
                                 **__) -> Dict[str, float]:
    """Resolve maximum severity in open vulnerability attribute."""
    max_open_severity = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['max_open_severity']
        )
    return \
        dict(max_open_severity=max_open_severity.get('max_open_severity', 0))


@get_entity_cache_async
async def _get_mean_remediate(_, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate."""
    mean_remediate = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate']
        )
    mean_remediate = mean_remediate.get('mean_remediate', 0)
    return dict(mean_remediate=mean_remediate)


@get_entity_cache_async
async def _get_mean_remediate_low_severity(
        _, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate_low_severity."""
    mean_remediate_low_severity = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate_low_severity']
        )
    mean_remediate_low_severity = mean_remediate_low_severity.get(
        'mean_remediate_low_severity', 0)
    return dict(mean_remediate_low_severity=mean_remediate_low_severity)


@get_entity_cache_async
async def _get_mean_remediate_medium_severity(
        _, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate_medium_severity."""
    mean_remediate_medium_severity = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate_medium_severity']
        )
    mean_remediate_medium_severity = mean_remediate_medium_severity.get(
        'mean_remediate_medium_severity', 0)
    return dict(mean_remediate_medium_severity=mean_remediate_medium_severity)


@get_entity_cache_async
async def _get_mean_remediate_high_severity(
        _, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate_high_severity."""
    mean_remediate_high_severity = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate_high_severity']
        )
    mean_remediate_high_severity = mean_remediate_high_severity.get(
        'mean_remediate_high_severity', 0)
    return dict(mean_remediate_high_severity=mean_remediate_high_severity)


@get_entity_cache_async
async def _get_mean_remediate_critical_severity(
        _, project_name: str, **__) -> Dict[str, int]:
    """Get mean_remediate_critical_severity."""
    mean_critical_remediate = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate_critical_severity']
        )
    mean_critical_remediate = mean_critical_remediate.get(
        'mean_remediate_critical_severity', 0)
    return dict(mean_remediate_critical_severity=mean_critical_remediate)


@get_entity_cache_async
async def _get_total_findings(info, project_name: str, **__) -> Dict[str, int]:
    """Get total_findings."""
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(
            project_domain.list_findings(project_name)
        )
    findings = \
        await info.context.loaders['finding'].load_many(finding_ids)

    total_findings = len([finding for finding in findings
                          if finding['current_state'] != 'DELETED'])
    return dict(total_findings=total_findings)


@get_entity_cache_async
async def _get_total_treatment(_, project_name: str, **__) -> Dict[str, str]:
    """Get total_treatment."""
    total_treatment = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['total_treatment']
        )
    total_treatment_decimal = total_treatment.get('total_treatment', {})
    total_treatment = json.dumps(
        total_treatment_decimal, use_decimal=True)
    return dict(total_treatment=total_treatment)


@get_entity_cache_async
async def _get_current_month_authors(_, project_name: str,
                                     **__) -> Dict[str, int]:
    """Get current_month_authors."""
    current_month_authors = await \
        sync_to_async(project_domain.get_current_month_authors)(
            project_name
        )
    return dict(current_month_authors=current_month_authors)


@get_entity_cache_async
async def _get_current_month_commits(_, project_name: str,
                                     **__) -> Dict[str, int]:
    """Get current_month_commits."""
    current_month_commits = await \
        sync_to_async(project_domain.get_current_month_commits)(
            project_name
        )
    return dict(current_month_commits=current_month_commits)


@get_entity_cache_async
async def _get_subscription(_, project_name: str, **__) -> Dict[str, str]:
    """Get subscription."""
    project_info = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['type']
        )
    subscription = project_info.get('type', '') if project_info else ''
    return dict(subscription=subscription)


@get_entity_cache_async
async def _get_deletion_date(_, project_name: str, **__) -> Dict[str, str]:
    """Get deletion_date."""
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    deletion_date = \
        historic_deletion[-1].get('deletion_date', '') \
        if historic_deletion else ''
    return dict(deletion_date=deletion_date)


@get_entity_cache_async
async def _get_user_deletion(_, project_name: str, **__) -> Dict[str, str]:
    """Get user_deletion."""
    user_deletion = ''
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    if historic_deletion and historic_deletion[-1].get('deletion_date'):
        user_deletion = historic_deletion[-1].get('user', '')
    return dict(user_deletion=user_deletion)


@get_entity_cache_async
async def _get_tags(_, project_name: str, **__) -> Dict[str, List[str]]:
    """Get tags."""
    project_data = await \
        sync_to_async(project_domain.get_attributes)(project_name, ['tag'])
    tags = \
        project_data['tag'] if project_data and 'tag' in project_data else []
    return dict(tags=tags)


@get_entity_cache_async
async def _get_description(_, project_name: str, **__)-> Dict[str, str]:
    """Get description."""
    description = await \
        sync_to_async(project_domain.get_description)(project_name)
    return dict(description=description)


@enforce_group_level_auth_async
async def _get_comments(
        info, project_name: str, **__) -> Dict[str, List[CommentType]]:
    """Get comments."""
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    comments = await sync_to_async(project_domain.list_comments)(
        project_name, user_email)
    return dict(comments=comments)


@enforce_group_level_auth_async
async def _get_drafts(
        info, project_name: str, **__) -> \
        Dict[str, List[Dict[str, FindingType]]]:
    """Get drafts."""
    await sync_to_async(util.cloudwatch_log)(
        info.context,
        f'Security: Access to {project_name} drafts')  # pragma: no cover
    finding_ids = await \
        sync_to_async(finding_domain.filter_deleted_findings)(
            project_domain.list_drafts(project_name)
        )
    findings = \
        await info.context.loaders['finding'].load_many(finding_ids)

    drafts = [draft for draft in findings
              if draft['current_state'] != 'DELETED']
    return dict(drafts=drafts)


@enforce_group_level_auth_async
async def _get_events(info,
                      project_name: str, **__) -> Dict[str, List[EventType]]:
    """Get events."""
    await sync_to_async(util.cloudwatch_log)(
        info.context,
        f'Security: Access to {project_name} events')  # pragma: no cover
    event_ids = await \
        sync_to_async(project_domain.list_events)(project_name)
    events = \
        await info.context.loaders['event'].load_many(event_ids)
    return dict(events=events)


@enforce_group_level_auth_async
async def _get_users(info, project_name: str,
                     requested_fields: list) -> Dict[str, List[UserType]]:
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
    user_roles_to_retrieve = ['customer', 'customeradmin']
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
    return dict(users=users)


async def resolve(info, project_name: str,
                  as_field: bool = False, as_list: bool = True) -> ProjectType:
    """Async resolve fields."""
    result: ProjectType = dict()
    tasks = list()
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
        future = asyncio.ensure_future(
            resolver_func(info, **params)
        )
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_project(_, info, project_name: str) -> ProjectType:
    """Resolve project query."""
    project_name = project_name.lower()
    return util.run_async(resolve, info, project_name)


@convert_kwargs_to_snake_case
def resolve_project_mutation(obj, info, **parameters):
    """Wrap project mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


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
        await sync_to_async(util.cloudwatch_log)(
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
        await sync_to_async(util.cloudwatch_log)(
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
        await sync_to_async(util.cloudwatch_log)(
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Added comment to '
            f'{project_name} project succesfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
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
            project_tags = \
                await sync_to_async(project_domain.get_attributes)(
                    project_name, ['tag'])
            project_tags = cast(ProjectType, project_tags)
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
            await sync_to_async(util.cloudwatch_log)(
                info.context, 'Security: \
Attempted to upload tags without the allowed structure')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
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
        project_tags = \
            await sync_to_async(project_domain.get_attributes)(
                project_name, ['tag'])
        project_tags = cast(ProjectType, project_tags)
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Removed tag from '
            f'{project_name} project succesfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
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
        await sync_to_async(util.cloudwatch_log)(
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
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Remove '
            f'all project access of {project_name}')  # pragma: no cover
        util.invalidate_cache(project_name)
    return SimplePayloadType(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
def resolve_alive_projects(_, info) -> List[ProjectType]:
    """Resolve for ACTIVE and SUSPENDED projects."""
    return util.run_async(_get_alive_projects, info)


async def _get_alive_projects(info) -> List[ProjectType]:
    """Resolve for ACTIVE and SUSPENDED projects."""
    alive_projects = await sync_to_async(project_domain.get_alive_projects)()
    return [await resolve(info, project) for project in alive_projects]
