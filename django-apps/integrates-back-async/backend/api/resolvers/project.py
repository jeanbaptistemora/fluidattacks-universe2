# pylint: disable=import-error

import asyncio
import sys

import simplejson as json
from asgiref.sync import sync_to_async
import rollbar

from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.event import EventLoader
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
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@sync_to_async
def _get_name(_, project_name):
    """Get name."""
    return dict(name=project_name)


@get_entity_cache_async
async def _get_remediated_over_time(_, project_name):
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
async def _get_has_drills(_, project_name):
    """Get has_drills."""
    attributes = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['has_drills']
        )
    return dict(has_drills=attributes.get('has_drills', False))


@get_entity_cache_async
async def _get_has_forces(_, project_name):
    """Get has_forces."""
    attributes = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['has_forces']
        )
    return dict(has_forces=attributes.get('has_forces', False))


@get_entity_cache_async
async def _get_findings(info, project_name):
    """Resolve findings attribute."""
    util.cloudwatch_log(info.context, 'Security: Access to {project} '
                        'findings'.format(project=project_name))
    finding_ids = await sync_to_async(finding_domain.filter_deleted_findings)(
        project_domain.list_findings(project_name)
    )
    findings = await info.context.loaders['finding'].load_many(finding_ids)
    findings = [finding for finding in findings
                if finding['current_state'] != 'DELETED']
    return dict(findings=findings)


@get_entity_cache_async
async def _get_open_vulnerabilities(info, project_name):
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
async def _get_closed_vulnerabilities(info, project_name):
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
async def _get_pending_closing_check(_, project_name):
    """Get pending_closing_check."""
    pending_closing_check = await \
        sync_to_async(project_domain.get_pending_closing_check)(project_name)
    return dict(pending_closing_check=pending_closing_check)


@get_entity_cache_async
async def _get_last_closing_vuln(_, project_name):
    """Get last_closing_vuln."""
    last_closing_vuln = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['last_closing_date']
        )
    last_closing_vuln = last_closing_vuln.get('last_closing_date', 0)
    return dict(last_closing_vuln=last_closing_vuln)


@get_entity_cache_async
async def _get_max_severity(info, project_name):
    """Get max_severity."""
    finding_ids = finding_domain.filter_deleted_findings(
        project_domain.list_findings(project_name))
    findings = \
        await info.context.loaders['finding'].load_many(finding_ids)

    max_severity = max(
        [finding['severity_score'] for finding in findings
         if finding['current_state'] != 'DELETED']) if findings else 0
    return dict(max_severity=max_severity)


@get_entity_cache_async
async def _get_mean_remediate(_, project_name):
    """Get mean_remediate."""
    mean_remediate = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['mean_remediate']
        )
    mean_remediate = mean_remediate.get('mean_remediate', 0)
    return dict(mean_remediate=mean_remediate)


@get_entity_cache_async
async def _get_total_findings(info, project_name):
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
async def _get_total_treatment(_, project_name):
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
async def _get_current_month_authors(_, project_name):
    """Get current_month_authors."""
    current_month_authors = await \
        sync_to_async(project_domain.get_current_month_authors)(
            project_name
        )
    return dict(current_month_authors=current_month_authors)


@get_entity_cache_async
async def _get_current_month_commits(_, project_name):
    """Get current_month_commits."""
    current_month_commits = await \
        sync_to_async(project_domain.get_current_month_commits)(
            project_name
        )
    return dict(current_month_commits=current_month_commits)


@get_entity_cache_async
async def _get_subscription(_, project_name):
    """Get subscription."""
    project_info = await \
        sync_to_async(project_domain.get_attributes)(
            project_name, ['type']
        )
    subscription = project_info.get('type', '') if project_info else ''
    return dict(subscription=subscription)


@get_entity_cache_async
async def _get_deletion_date(_, project_name):
    """Get deletion_date."""
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    deletion_date = \
        historic_deletion[-1].get('deletion_date', '') \
        if historic_deletion else ''
    return dict(deletion_date=deletion_date)


@get_entity_cache_async
async def _get_user_deletion(_, project_name):
    """Get user_deletion."""
    user_deletion = ''
    historic_deletion = await \
        sync_to_async(project_domain.get_historic_deletion)(project_name)
    if historic_deletion and historic_deletion[-1].get('deletion_date'):
        user_deletion = historic_deletion[-1].get('user', '')
    return dict(user_deletion=user_deletion)


@get_entity_cache_async
async def _get_tags(_, project_name):
    """Get tags."""
    project_data = await \
        sync_to_async(project_domain.get_attributes)(project_name, ['tag'])
    tags = \
        project_data['tag'] if project_data and 'tag' in project_data else []
    return dict(tags=tags)


@get_entity_cache_async
async def _get_description(_, project_name):
    """Get description."""
    description = await \
        sync_to_async(project_domain.get_description)(project_name)
    return dict(description=description)


async def _resolve_fields(info, project_name):
    """Async resolve fields."""
    loaders = {
        'finding': FindingLoader(),
        'vulnerability': VulnerabilityLoader(),
        'event': EventLoader(),
    }
    info.context.loaders = loaders
    result = dict()
    tasks = list()
    for requested_field in info.field_nodes[0].selection_set.selections:
        snake_field = convert_camel_case_to_snake(requested_field.name.value)
        if snake_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snake_field}'
        )
        future = asyncio.ensure_future(
            resolver_func(info, project_name=project_name)
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
def resolve_project(_, info, project_name):
    """Resolve project query."""
    return util.run_async(_resolve_fields, info, project_name)


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
