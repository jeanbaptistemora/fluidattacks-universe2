# pylint: disable=import-error

import asyncio
import re
import sys

import rollbar
from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.dataloaders.finding import FindingLoader

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, rename_kwargs,
    require_login, require_finding_access, require_project_access
)
from backend.domain import (
    comment as comment_domain, finding as finding_domain,
    project as project_domain, user as user_domain,
    vulnerability as vuln_domain
)
from backend.utils import findings as finding_utils
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


def extract_id(body):
    """Extract identifier from query."""
    body = body.decode()
    match = re.search(r'finding\(identifier: (?:\\|)"([0-9]+)(?:\\|)"\)', body)
    if match:
        return match.group(1)
    raise GraphQLError('Could not resolve finding identifier.')


@get_entity_cache_async
async def _get_vulnerabilities(
    info, vuln_type, state, approval_status
):
    """Get vulnerabilities."""
    identifier = extract_id(info.context.body)
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    if vuln_type:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered if vuln.vuln_type == vuln_type
             and (vuln['current_approval_status'] != 'PENDING' or
                  vuln['last_approved_status'])]
    if state:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered
             if vuln_domain.get_current_state(vuln) == state and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])]
    if approval_status:
        vuln_filtered = \
            {vuln for vuln in vuln_filtered
             if vuln['current_approval_status'] == approval_status}
    return vuln_filtered


async def _resolve_vulnerabilities(
    info, vuln_type, state, approval_status
):
    """Async resolve fields."""
    loaders = {
        'finding': FindingLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    info.context.loaders = loaders
    future = asyncio.ensure_future(
        _get_vulnerabilities(info, vuln_type, state, approval_status)
    )
    tasks_result = await asyncio.gather(future)
    return tasks_result[0]


@convert_kwargs_to_snake_case
def resolve_vulnerabilities(
    _, info, vuln_type=None, state=None, approval_status=None
):
    """Resolve vulnerabilities field."""
    return util.run_async(
        _resolve_vulnerabilities, info, vuln_type, state, approval_status
    )


@sync_to_async
def _get_id(_, identifier):
    """Get id."""
    return dict(id=identifier)


@get_entity_cache_async
async def _get_project_name(info, identifier):
    """Get project_name."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(project_name=finding['project_name'])


@get_entity_cache_async
async def _get_open_vulnerabilities(info, identifier):
    """Get open_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    open_vulnerabilities = len([
        vuln for vuln in vulns
        if await sync_to_async(vuln_domain.get_current_state)(vuln) == 'open'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(open_vulnerabilities=open_vulnerabilities)


@get_entity_cache_async
async def _get_closed_vulnerabilities(info, identifier):
    """Get closed_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    closed_vulnerabilities = len([
        vuln for vuln in vulns
        if await sync_to_async(vuln_domain.get_current_state)(vuln) == 'closed'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(closed_vulnerabilities=closed_vulnerabilities)


@get_entity_cache_async
async def _get_release_date(info, identifier):
    """Get release date."""
    allowed_roles = ['admin', 'analyst']
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    if not release_date and curr_user_role not in allowed_roles:
        raise GraphQLError('Access denied')
    return dict(release_date=release_date)


@get_entity_cache_async
async def _get_tracking(info, identifier):
    """Get tracking."""
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    if release_date:
        vulns = await info.context.loaders['vulnerability'].load(identifier)
        tracking = \
            await \
            sync_to_async(finding_domain.get_tracking_vulnerabilities)(vulns)
    else:
        tracking = []
    return dict(tracking=tracking)


@get_entity_cache_async
async def _get_records(info, identifier):
    """Get records."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['records']['url']:
        records = await sync_to_async(finding_utils.get_records_from_file)(
            finding['project_name'], finding['id'], finding['records']['url'])
    else:
        records = []
    return dict(records=records)


@get_entity_cache_async
async def _get_severity(info, identifier):
    """Get severity."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(severity=finding['severity'])


@get_entity_cache_async
async def _get_cvss_version(info, identifier):
    """Get cvss_version."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(cvss_version=finding['cvss_version'])


@get_entity_cache_async
async def _get_exploit(info, identifier):
    """Get exploit."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['exploit']['url']:
        exploit = \
            await \
            sync_to_async(finding_utils.get_exploit_from_file)(
                finding['project_name'], finding['id'],
                finding['exploit']['url'])
    else:
        exploit = ''
    return dict(exploit=exploit)


@get_entity_cache_async
async def _get_evidence(info, identifier):
    """Get evidence."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(evidence=finding['evidence'])


@get_entity_cache_async
async def _get_comments(info, identifier):
    """Get comments."""
    finding = await info.context.loaders['finding'].load(identifier)
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    comments = await sync_to_async(comment_domain.get_comments)(
        finding['id'], curr_user_role
    )
    return dict(comments=comments)


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_observations(info, identifier):
    """Get observations."""
    finding = await info.context.loaders['finding'].load(identifier)
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    observations = await sync_to_async(comment_domain.get_observations)(
        finding['id'], curr_user_role
    )
    return dict(observations=observations)


@get_entity_cache_async
async def _get_state(info, identifier):
    """Get state."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    state = 'open' \
        if [vuln for vuln in vulns
            if await sync_to_async(vuln_domain.get_last_approved_status)(vuln)
            == 'open'] \
        else 'closed'
    return dict(state=state)


@get_entity_cache_async
async def _get_last_vulnerability(info, identifier):
    """Get last_vulnerability."""
    finding = await info.context.loaders['finding'].load(identifier)
    last_vuln_date = \
        util.calculate_datediff_since(finding['last_vulnerability'])
    last_vulnerability = last_vuln_date.days
    return dict(last_vulnerability=last_vulnerability)


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_historic_state(info, identifier):
    """Get historic_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(historic_state=finding['historic_state'])


@get_entity_cache_async
async def _get_title(info, identifier):
    """Get title."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(title=finding['title'])


@get_entity_cache_async
async def _get_scenario(info, identifier):
    """Get scenario."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(scenario=finding['scenario'])


@get_entity_cache_async
async def _get_actor(info, identifier):
    """Get actor."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(actor=finding['actor'])


@get_entity_cache_async
async def _get_description(info, identifier):
    """Get description."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(description=finding['description'])


@get_entity_cache_async
async def _get_requirements(info, identifier):
    """Get requirements."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(requirements=finding['requirements'])


@get_entity_cache_async
async def _get_attack_vector_desc(info, identifier):
    """Get attack_vector_desc."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(attack_vector_desc=finding['attack_vector_desc'])


@get_entity_cache_async
async def _get_threat(info, identifier):
    """Get threat."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(threat=finding['threat'])


@get_entity_cache_async
async def _get_recommendation(info, identifier):
    """Get recommendation."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(recommendation=finding['recommendation'])


@get_entity_cache_async
async def _get_affected_systems(info, identifier):
    """Get affected_systems."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(affected_systems=finding['affected_systems'])


@get_entity_cache_async
async def _get_compromised_attributes(info, identifier):
    """Get compromised_attributes."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(compromised_attributes=finding['compromised_attributes'])


@get_entity_cache_async
async def _get_compromised_records(info, identifier):
    """Get compromised_records."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(compromised_records=finding['compromised_records'])


@get_entity_cache_async
async def _get_cwe_url(info, identifier):
    """Get cwe_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(cwe_url=finding['cwe_url'])


@get_entity_cache_async
async def _get_bts_url(info, identifier):
    """Get bts_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(bts_url=finding['bts_url'])


@get_entity_cache_async
async def _get_risk(info, identifier):
    """Get risk."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(risk=finding['risk'])


@get_entity_cache_async
async def _get_remediated(info, identifier):
    """Get remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(remediated=finding['remediated'])


@get_entity_cache_async
async def _get_type(info, identifier):
    """Get type."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(type=finding['type'])


@get_entity_cache_async
async def _get_age(info, identifier):
    """Get age."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(age=finding['age'])


@get_entity_cache_async
async def _get_is_exploitable(info, identifier):
    """Get is_exploitable."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(is_exploitable=finding['is_exploitable'])


@get_entity_cache_async
async def _get_severity_score(info, identifier):
    """Get severity_score."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(severity_score=finding['severity_score'])


@get_entity_cache_async
async def _get_report_date(info, identifier):
    """Get report_date."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(report_date=finding['report_date'])


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_analyst(info, identifier):
    """Get analyst."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(analyst=finding['analyst'])


@get_entity_cache_async
async def _get_historic_treatment(info, identifier):
    """Get historic_treatment."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(historic_treatment=finding['historic_treatment'])


@get_entity_cache_async
async def _get_current_state(info, identifier):
    """Get current_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(current_state=finding['current_state'])


@get_entity_cache_async
async def _get_new_remediated(info, identifier):
    """Get new_remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(new_remediated=finding['new_remediated'])


@get_entity_cache_async
async def _get_verified(info, identifier):
    """Get verified."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(verified=finding['verified'])


async def _resolve_fields(info, identifier):
    """Async resolve fields."""
    loaders = {
        'finding': FindingLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    info.context.loaders = loaders
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
        future = asyncio.ensure_future(
            resolver_func(info, identifier=identifier)
        )
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@require_finding_access
@rename_kwargs({'finding_id': 'identifier'})
def resolve_finding(_, info, identifier):
    """Resolve finding query."""
    return util.run_async(_resolve_fields, info, identifier)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
@enforce_group_level_auth_async
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
