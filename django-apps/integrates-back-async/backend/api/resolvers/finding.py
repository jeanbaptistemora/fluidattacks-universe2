from collections import namedtuple
from time import time
import sys
from typing import Any, Dict, List, cast

import rollbar

from asgiref.sync import sync_to_async
from graphql.language.ast import SelectionSetNode
from graphql import GraphQLError

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, rename_kwargs,
    require_login, require_finding_access, require_project_access
)
from backend.domain import (
    comment as comment_domain,
    finding as finding_domain,
    project as project_domain,
    user as user_domain,
    vulnerability as vuln_domain
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
    AddCommentPayload as AddCommentPayloadType,
    Vulnerability as VulnerabilityType,
)
from backend.utils import findings as finding_utils
from backend import util

from ariadne import convert_camel_case_to_snake, convert_kwargs_to_snake_case


@get_entity_cache_async
async def _get_vulnerabilities(info, identifier: str,
                               state: str = '') -> List[VulnerabilityType]:
    """Get vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    if state:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered
             if vuln['current_state'] == state and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_ports_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get ports vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'ports'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_inputs_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get inputs vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'inputs'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_lines_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get lines vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'lines'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_pending_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get pending vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    vuln_filtered = \
        [vuln for vuln in vuln_filtered
            if vuln['current_approval_status'] == 'PENDING']
    return vuln_filtered


@sync_to_async
def _get_id(_, identifier: str) -> str:
    """Get id."""
    return identifier


@get_entity_cache_async
async def _get_project_name(info, identifier: str) -> str:
    """Get project_name."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['project_name']


@get_entity_cache_async
async def _get_open_vulnerabilities(info, identifier: str) -> int:
    """Get open_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    open_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln['current_state'] == 'open'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return open_vulnerabilities


@get_entity_cache_async
async def _get_closed_vulnerabilities(info, identifier: str) -> int:
    """Get closed_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    closed_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln['current_state'] == 'closed'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return closed_vulnerabilities


@get_entity_cache_async
async def _get_release_date(info, identifier: str) -> str:
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
    return release_date


@get_entity_cache_async
async def _get_tracking(info, identifier: str) -> List[Dict[str, int]]:
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
    return tracking


@get_entity_cache_async
async def _get_records(info, identifier: str) -> List[Dict[object, object]]:
    """Get records."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['records']['url']:
        records = await sync_to_async(finding_utils.get_records_from_file)(
            finding['project_name'], finding['id'], finding['records']['url'])
    else:
        records = []
    return records


@get_entity_cache_async
async def _get_severity(info, identifier: str) -> Dict[str, str]:
    """Get severity."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['severity']


@get_entity_cache_async
async def _get_cvss_version(info, identifier: str) -> str:
    """Get cvss_version."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['cvss_version']


@get_entity_cache_async
async def _get_exploit(info, identifier: str) -> str:
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
    return exploit


@get_entity_cache_async
async def _get_evidence(info, identifier: str) -> Dict[str, Dict[str, str]]:
    """Get evidence."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['evidence']


@get_entity_cache_async
async def _get_comments(info, identifier: str) -> List[CommentType]:
    """Get comments."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding.get('project_name')
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    comments = await sync_to_async(comment_domain.get_comments)(
        project_name, finding_id, user_email
    )
    return comments


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_observations(info, identifier: str) -> List[CommentType]:
    """Get observations."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding['project_name']
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    observations = await sync_to_async(comment_domain.get_observations)(
        project_name, finding_id, user_email
    )
    return observations


@get_entity_cache_async
async def _get_state(info, identifier: str) -> str:
    """Get state."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    state = 'open' \
        if [vuln for vuln in vulns
            if await sync_to_async(vuln_domain.get_last_approved_status)(vuln)
            == 'open'] \
        else 'closed'
    return state


@get_entity_cache_async
async def _get_last_vulnerability(info, identifier: str) -> int:
    """Get last_vulnerability."""
    finding = await info.context.loaders['finding'].load(identifier)
    last_vuln_date = \
        util.calculate_datediff_since(finding['last_vulnerability'])
    return last_vuln_date.days


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_historic_state(info, identifier: str) -> List[Dict[str, str]]:
    """Get historic_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['historic_state']


@get_entity_cache_async
async def _get_title(info, identifier: str) -> str:
    """Get title."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['title']


@get_entity_cache_async
async def _get_scenario(info, identifier: str) -> str:
    """Get scenario."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['scenario']


@get_entity_cache_async
async def _get_actor(info, identifier: str) -> str:
    """Get actor."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['actor']


@get_entity_cache_async
async def _get_description(info, identifier: str) -> str:
    """Get description."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['description']


@get_entity_cache_async
async def _get_requirements(info, identifier: str) -> str:
    """Get requirements."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['requirements']


@get_entity_cache_async
async def _get_attack_vector_desc(info, identifier: str) -> str:
    """Get attack_vector_desc."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['attack_vector_desc']


@get_entity_cache_async
async def _get_threat(info, identifier: str) -> str:
    """Get threat."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['threat']


@get_entity_cache_async
async def _get_recommendation(info, identifier: str) -> str:
    """Get recommendation."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['recommendation']


@get_entity_cache_async
async def _get_affected_systems(info, identifier: str) -> str:
    """Get affected_systems."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['affected_systems']


@get_entity_cache_async
async def _get_compromised_attributes(info, identifier: str) -> str:
    """Get compromised_attributes."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['compromised_attributes']


@get_entity_cache_async
async def _get_compromised_records(info, identifier: str) -> int:
    """Get compromised_records."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['compromised_records']


@get_entity_cache_async
async def _get_cwe_url(info, identifier: str) -> str:
    """Get cwe_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['cwe_url']


@get_entity_cache_async
async def _get_bts_url(info, identifier: str) -> str:
    """Get bts_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['bts_url']


@get_entity_cache_async
async def _get_risk(info, identifier: str) -> str:
    """Get risk."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['risk']


@get_entity_cache_async
async def _get_remediated(info, identifier: str) -> bool:
    """Get remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['remediated']


@get_entity_cache_async
async def _get_type(info, identifier: str) -> str:
    """Get type."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['type']


@get_entity_cache_async
async def _get_age(info, identifier: str) -> int:
    """Get age."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['age']


@get_entity_cache_async
async def _get_is_exploitable(info, identifier: str) -> bool:
    """Get is_exploitable."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['is_exploitable']


@get_entity_cache_async
async def _get_severity_score(info, identifier: str) -> float:
    """Get severity_score."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['severity_score']


@get_entity_cache_async
async def _get_report_date(info, identifier: str) -> str:
    """Get report_date."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['report_date']


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_analyst(info, identifier: str) -> str:
    """Get analyst."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['analyst']


@get_entity_cache_async
async def _get_historic_treatment(info,
                                  identifier: str) -> List[Dict[str, str]]:
    """Get historic_treatment."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['historic_treatment']


@get_entity_cache_async
async def _get_current_state(info, identifier: str) -> str:
    """Get current_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['current_state']


@get_entity_cache_async
async def _get_new_remediated(info, identifier: str) -> bool:
    """Get new_remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['new_remediated']


@get_entity_cache_async
async def _get_verified(info, identifier: str) -> bool:
    """Get verified."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['verified']


async def resolve(
        info, identifier: str, as_field: bool = False,
        selection_set: SelectionSetNode = SelectionSetNode()) -> \
        Dict[str, FindingType]:
    """Async resolve fields."""
    result = dict()
    requested_fields = \
        selection_set.selections if as_field else \
        info.field_nodes[0].selection_set.selections

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


@convert_kwargs_to_snake_case
def resolve_finding_mutation(obj, info, **parameters):
    """Resolve findings mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return resolver_func(obj, info, **parameters)


@convert_kwargs_to_snake_case
@require_login
@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@require_finding_access
@rename_kwargs({'finding_id': 'identifier'})
async def resolve_finding(_, info, identifier: str) -> Dict[str, FindingType]:
    """Resolve finding query."""
    return await resolve(info, identifier)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_remove_evidence(_, info, evidence_id: str,
                              finding_id: str) -> SimpleFindingPayloadType:
    """Resolve remove_evidence mutation."""
    success = await \
        sync_to_async(finding_domain.remove_evidence)(evidence_id, finding_id)

    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: \
Removed evidence in finding {finding_id}')  # pragma: no cover
        util.invalidate_cache(finding_id)
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_update_evidence(_, info, evidence_id: str, finding_id: str,
                              file) -> SimplePayloadType:
    """Resolve update_evidence mutation."""
    success = False

    if await \
            sync_to_async(finding_domain.validate_evidence)(evidence_id, file):
        success = await sync_to_async(finding_domain.update_evidence)(
            finding_id, evidence_id, file)
    if success:
        util.invalidate_cache(finding_id)
        util.cloudwatch_log(
            info.context,
            'Security: Updated evidence in finding '
            f'{finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to update evidence in '
            f'finding {finding_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_update_evidence_description(
        _, info, finding_id: str, evidence_id: str,
        description: str) -> SimplePayloadType:
    """Resolve update_evidence_description mutation."""
    success = False
    try:
        success = await \
            sync_to_async(finding_domain.update_evidence_description)(
                finding_id, evidence_id, description)
        if success:
            util.invalidate_cache(finding_id)
            util.cloudwatch_log(
                info.context, f'Security: Evidence description \
succesfully updated in finding {finding_id}')  # pragma: no cover
        else:
            util.cloudwatch_log(
                info.context, f'Security: Attempted to update \
                evidence description in {finding_id}')  # pragma: no cover
    except KeyError:
        await sync_to_async(rollbar.report_message)('Error: \
An error occurred updating evidence description', 'error', info.context)
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_update_severity(_, info,
                              **parameters) -> SimpleFindingPayloadType:
    """Perform update_severity mutation."""
    data = parameters.get('data', dict())
    data = {util.snakecase_to_camelcase(k): data[k] for k in data}
    finding_id = parameters.get('finding_id', '')
    project = await sync_to_async(finding_domain.get_project)(finding_id)
    success = False
    success = await sync_to_async(finding_domain.save_severity)(data)
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project)
        util.cloudwatch_log(
            info.context, f'Security: Updated severity in \
            finding {finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to update \
            severity in finding {finding_id}')  # pragma: no cover
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_add_finding_comment(_, info,
                                  **parameters) -> AddCommentPayloadType:
    """Perform add_finding_comment mutation."""
    param_type = parameters.get('type', '').lower()
    if param_type in ['comment', 'observation']:
        user_data = util.get_jwt_content(info.context)
        user_email = user_data['user_email']
        finding_id = parameters.get('finding_id')
        finding = await sync_to_async(finding_domain.get_finding)(finding_id)
        group = finding.get('projectName')
        role = \
            user_domain.get_group_level_role(user_email, group)
        if param_type == 'observation' and \
                role not in ['analyst', 'admin']:
            util.cloudwatch_log(info.context, 'Security: \
Unauthorized role attempted to add observation')  # pragma: no cover
            raise GraphQLError('Access denied')

        user_email = user_data['user_email']
        comment_id = int(round(time() * 1000))
        comment_data = {
            'user_id': comment_id,
            'comment_type': param_type,
            'content': parameters.get('content'),
            'fullname': str.join(' ', [user_data['first_name'],
                                 user_data['last_name']]),
            'parent': parameters.get('parent'),
        }
        success = await sync_to_async(finding_domain.add_comment)(
            user_email=user_email,
            comment_data=comment_data,
            finding_id=finding_id,
            is_remediation_comment=False
        )
    else:
        raise GraphQLError('Invalid comment type')
    if success:
        util.invalidate_cache(parameters.get('finding_id', ''))
        util.cloudwatch_log(info.context, f'Security: Added comment in\
            finding {finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to add \
comment in finding {finding_id}')  # pragma: no cover
    ret = AddCommentPayloadType(success=success, comment_id=str(comment_id))
    return ret


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_handle_acceptation(_, info, **parameters) -> SimplePayloadType:
    """Resolve handle_acceptation mutation."""
    user_info = util.get_jwt_content(info.context)
    user_mail = user_info['user_email']
    finding_id = parameters.get('finding_id', '')
    historic_treatment = await \
        sync_to_async(finding_domain.get_finding_historic_treatment)(
            finding_id
        )
    if historic_treatment[-1]['acceptance_status'] != 'SUBMITTED':
        raise GraphQLError(
            'It cant be approved/rejected a finding' +
            'definite assumption without being requested')

    success = await \
        sync_to_async(finding_domain.handle_acceptation)(
            finding_id, parameters.get('observations'), user_mail,
            parameters.get('response')
        )
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(parameters.get('project_name', ''))
        util.forces_trigger_deployment(parameters.get('project_name', ''))
        util.cloudwatch_log(
            info.context, 'Security: Verified a request '
            f'in finding_id: {finding_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_update_description(_, info, finding_id: str,
                                 **parameters) -> SimpleFindingPayloadType:
    """Perform update_description mutation."""
    success = await \
        sync_to_async(finding_domain.update_description)(
            finding_id, parameters
        )
    if success:
        project_name = await \
            sync_to_async(project_domain.get_finding_project_name)(finding_id)
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context, f'Security: Updated description in \
finding {finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to update \
            description in finding {finding_id}')  # pragma: no cover
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_update_client_description(
        _, info, finding_id: str, **parameters) -> SimpleFindingPayloadType:
    """Perform update_client_description mutation."""
    finding = await \
        sync_to_async(finding_domain.get_finding)(finding_id)
    project_name = finding['projectName']
    user_mail = util.get_jwt_content(info.context)['user_email']
    if parameters.get('acceptance_status') == '':
        del parameters['acceptance_status']
    historic_treatment = finding['historicTreatment']
    last_state = {
        key: value for key, value in historic_treatment[-1].items()
        if key not in ['date', 'user']}
    new_state = {
        key: value for key, value in parameters.items() if key != 'bts_url'}
    bts_changed, treatment_changed = True, True
    Status = namedtuple('Status', 'bts_changed treatment_changed')
    if not await \
        sync_to_async(finding_domain.compare_historic_treatments)(
            last_state, new_state):
        treatment_changed = False
    if 'externalBts' in finding and \
            parameters.get('bts_url') == finding['externalBts']:
        bts_changed = False
    update = Status(bts_changed=bts_changed,
                    treatment_changed=treatment_changed)
    if not any(list(update)):
        raise GraphQLError(
            'It cant be updated a finding with same values it already has'
        )
    success = await \
        sync_to_async(finding_domain.update_client_description)(
            finding_id, parameters, user_mail, update
        )
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context, 'Security: Updated treatment in '
            f'finding {finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, 'Security: Attempted to update '
            f'treatment in finding {finding_id}')  # pragma: no cover
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_reject_draft(_, info, finding_id: str) -> SimplePayloadType:
    """Resolve reject_draft mutation."""
    reviewer_email = util.get_jwt_content(info.context)['user_email']
    project_name = await \
        sync_to_async(project_domain.get_finding_project_name)(finding_id)

    success = await \
        sync_to_async(finding_domain.reject_draft)(finding_id, reviewer_email)
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Draft {finding_id} \
rejected succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to reject \
draft {finding_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_delete_finding(_, info, finding_id: str,
                             justification: str) -> SimplePayloadType:
    """Resolve delete_finding mutation."""
    project_name = await \
        sync_to_async(project_domain.get_finding_project_name)(finding_id)

    success = await \
        sync_to_async(finding_domain.delete_finding)(
            finding_id, project_name, justification, info.context)
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Deleted finding: \
{finding_id} succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to delete \
finding: {finding_id}')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
async def _do_approve_draft(_, info, draft_id: str) -> ApproveDraftPayloadType:
    """Resolve approve_draft mutation."""
    reviewer_email = util.get_jwt_content(info.context)['user_email']
    project_name = await \
        sync_to_async(project_domain.get_finding_project_name)(draft_id)

    has_vulns = [
        vuln for vuln in
        await vuln_domain.list_vulnerabilities_async([draft_id])
        if cast(List[Dict[str, Any]],
                vuln['historic_state'])[-1].get('state') != 'DELETED']
    if not has_vulns:
        raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
    success, release_date = await sync_to_async(finding_domain.approve_draft)(
        draft_id, reviewer_email)
    if success:
        util.invalidate_cache(draft_id)
        util.invalidate_cache(project_name)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context, f'Security: Approved draft in \
            {project_name} project succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to approve \
            draft in {project_name} project')  # pragma: no cover
    return ApproveDraftPayloadType(release_date=release_date, success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_create_draft(_, info, project_name: str, title: str,
                           **kwargs) -> SimplePayloadType:
    """Resolve create_draft mutation."""
    success = await \
        sync_to_async(finding_domain.create_draft)(
            info, project_name, title, **kwargs)
    if success:
        util.cloudwatch_log(
            info.context, 'Security: Created draft in '
            f'{project_name} project succesfully')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_submit_draft(_, info, finding_id: str) -> SimplePayloadType:
    """Resolve submit_draft mutation."""
    analyst_email = util.get_jwt_content(info.context)['user_email']
    success = await \
        sync_to_async(finding_domain.submit_draft)(finding_id, analyst_email)

    if success:
        util.invalidate_cache(finding_id)
        util.cloudwatch_log(
            info.context, 'Security: Submitted draft '
            f'{finding_id} succesfully')  # pragma: no cover
    return SimplePayloadType(success=success)
