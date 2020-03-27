# pylint: disable=import-error

import asyncio
import sys

import rollbar
from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.dataloaders.finding import FindingLoader

from backend.decorators import (
    enforce_authz_async, rename_kwargs, require_login,
    require_finding_access, require_project_access
)
from backend.domain import (
    finding as finding_domain, project as project_domain,
    vulnerability as vuln_domain
)
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@sync_to_async
def _get_id(_, identifier):
    """Get id."""
    return dict(id=identifier)


async def _get_project_name(_, identifier):
    """Get project_name."""
    finding = await FindingLoader().load(identifier)
    return dict(project_name=finding['project_name'])


async def _get_open_vulnerabilities(_, identifier):
    """Get open_vulnerabilities."""
    vulns = await VulnerabilityLoader().load(identifier)

    open_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln_domain.get_current_state(vuln) == 'open' and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(open_vulnerabilities=open_vulnerabilities)


async def _get_closed_vulnerabilities(_, identifier):
    """Get closed_vulnerabilities."""
    vulns = await VulnerabilityLoader().load(identifier)

    closed_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln_domain.get_current_state(vuln) == 'closed' and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(closed_vulnerabilities=closed_vulnerabilities)


async def _get_release_date(info, identifier):
    """Get release date."""
    allowed_roles = ['admin', 'analyst']
    finding = await FindingLoader().load(identifier)
    release_date = finding['release_date']
    if not release_date and \
            util.get_jwt_content(info.context)['user_role'] \
            not in allowed_roles:
        raise GraphQLError('Access denied')
    return dict(release_date=release_date)


async def _resolve_fields(info, identifier):
    """Async resolve fields."""
    result = dict()
    tasks = list()
    for requested_field in info.field_nodes[0].selection_set.selections:
        snake_field = convert_camel_case_to_snake(requested_field.name.value)
        if snake_field.startswith('_') or snake_field == 'vulnerabilities':
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snake_field}'
        )
        future = asyncio.ensure_future(resolver_func(info, identifier))
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@rename_kwargs({'identifier': 'finding_id'})
@enforce_authz_async
@require_finding_access
@rename_kwargs({'finding_id': 'identifier'})
def resolve_finding(_, info, identifier):
    """Resolve finding query."""
    return util.run_async(_resolve_fields, info, identifier)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_remove_evidence(_, info, evidence_id, finding_id):
    """Resolve remove_evidence mutation."""
    success = finding_domain.remove_evidence(evidence_id, finding_id)

    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Removed evidence in finding {finding_id}')
        util.invalidate_cache(finding_id)
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_update_evidence(_, info, evidence_id, finding_id, file):
    """Resolve update_evidence mutation."""
    success = False

    if finding_domain.validate_evidence(evidence_id, file):
        success = finding_domain.update_evidence(
            finding_id, evidence_id, file)
    if success:
        util.invalidate_cache(finding_id)
        util.cloudwatch_log(info.context,
                            'Security: Updated evidence in finding '
                            f'{finding_id} succesfully')
    else:
        util.cloudwatch_log(info.context,
                            'Security: Attempted to update evidence in '
                            f'finding {finding_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_update_evidence_description(
    _, info, finding_id, evidence_id, description
):
    """Resolve update_evidence_description mutation."""
    success = False
    try:
        success = finding_domain.update_evidence_description(
            finding_id, evidence_id, description)
        if success:
            util.invalidate_cache(finding_id)
            util.cloudwatch_log(info.context, 'Security: Evidence description \
                succesfully updated in finding ' + finding_id)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to update \
                evidence description in ' + finding_id)
    except KeyError:
        rollbar.report_message('Error: \
An error occurred updating evidence description', 'error', info.context)
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_verify_finding(_, info, finding_id, justification):
    """Resolve verify_finding mutation."""
    project_name = project_domain.get_finding_project_name(finding_id)
    user_info = util.get_jwt_content(info.context)
    success = finding_domain.verify_finding(
        finding_id, user_info['user_email'],
        justification,
        str.join(' ', [user_info['first_name'], user_info['last_name']])
    )
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(info.context, 'Security: Verified the '
                            f'finding_id: {finding_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_handle_acceptation(_, info, **parameters):
    """Resolve handle_acceptation mutation."""
    user_info = util.get_jwt_content(info.context)
    user_mail = user_info['user_email']
    finding_id = parameters.get('finding_id')
    historic_treatment = \
        finding_domain.get_finding(finding_id).get('historicTreatment')
    if historic_treatment[-1]['acceptance_status'] != 'SUBMITTED':
        raise GraphQLError(
            'It cant be approved/rejected a finding' +
            'definite assumption without being requested')

    success = finding_domain.handle_acceptation(finding_id,
                                                parameters.get('observations'),
                                                user_mail,
                                                parameters.get('response'))
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(parameters.get('project_name'))
        util.cloudwatch_log(info.context, 'Security: Verified a request '
                            f'in finding_id: {finding_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_reject_draft(_, info, finding_id):
    """Resolve reject_draft mutation."""
    reviewer_email = util.get_jwt_content(info.context)['user_email']
    project_name = finding_domain.get_finding(finding_id)['projectName']

    success = finding_domain.reject_draft(finding_id, reviewer_email)
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            'Security: Draft {} rejected succesfully'.format(finding_id))
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to reject draft {}'.format(finding_id))
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_delete_finding(_, info, finding_id, justification):
    """Resolve delete_finding mutation."""
    project_name = finding_domain.get_finding(finding_id)['projectName']

    success = finding_domain.delete_finding(
        finding_id, project_name, justification, info.context)
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Deleted finding: {finding_id} succesfully')
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to delete finding: {finding_id}')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
def resolve_approve_draft(_, info, draft_id):
    """Resolve approve_draft mutation."""
    reviewer_email = util.get_jwt_content(info.context)['user_email']
    project_name = finding_domain.get_finding(draft_id)['projectName']

    has_vulns = [vuln for vuln in vuln_domain.list_vulnerabilities([draft_id])
                 if vuln['historic_state'][-1].get('state') != 'DELETED']
    if not has_vulns:
        raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
    success, release_date = finding_domain.approve_draft(
        draft_id, reviewer_email)
    if success:
        util.invalidate_cache(draft_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(info.context, 'Security: Approved draft in\
            {project} project succesfully'.format(project=project_name))
    else:
        util.cloudwatch_log(info.context, 'Security: Attempted to approve \
            draft in {project} project'.format(project=project_name))
    return dict(release_date=release_date, success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_project_access
def resolve_create_draft(_, info, project_name, title, **kwargs):
    """Resolve create_draft mutation."""
    success = finding_domain.create_draft(
        info, project_name, title, **kwargs)
    if success:
        util.cloudwatch_log(info.context, 'Security: Created draft in '
                            '{} project succesfully'.format(project_name))
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_submit_draft(_, info, finding_id):
    """Resolve submit_draft mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = finding_domain.submit_draft(finding_id, analyst_email)

    if success:
        util.invalidate_cache(finding_id)
        util.cloudwatch_log(info.context, 'Security: Submitted draft '
                            '{} succesfully'.format(finding_id))
    return dict(success=success)
