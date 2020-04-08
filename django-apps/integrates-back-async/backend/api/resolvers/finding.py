# pylint: disable=import-error

from collections import namedtuple
import sys
from typing import Any, Dict, List, cast

import rollbar

from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend.api.dataloaders import finding as finding_loader

from backend.decorators import (
    enforce_group_level_auth_async, rename_kwargs,
    require_login, require_finding_access, require_project_access
)
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    vulnerability as vuln_domain
)
from backend.typing import (
    Finding as FindingType,
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
)
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_finding_mutation(obj, info, **parameters):
    """Resolve update_severity mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@convert_kwargs_to_snake_case
@require_login
@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@require_finding_access
@rename_kwargs({'finding_id': 'identifier'})
def resolve_finding(_, info, identifier: str) -> Dict[str, FindingType]:
    """Resolve finding query."""
    return util.run_async(finding_loader.resolve, info, identifier)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_remove_evidence(_, info, evidence_id: str,
                              finding_id: str) -> SimpleFindingPayloadType:
    """Resolve remove_evidence mutation."""
    success = await \
        sync_to_async(finding_domain.remove_evidence)(evidence_id, finding_id)

    if success:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Removed evidence in finding {finding_id}')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Updated evidence in finding '
            f'{finding_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to update evidence in '
            f'finding {finding_id}')
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
            await sync_to_async(util.cloudwatch_log)(
                info.context, f'Security: Evidence description \
                succesfully updated in finding {finding_id}')
        else:
            await sync_to_async(util.cloudwatch_log)(
                info.context, f'Security: Attempted to update \
                evidence description in {finding_id}')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Updated severity in \
            finding {finding_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to update \
            severity in finding {finding_id}')
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@require_login
@enforce_group_level_auth_async
@require_finding_access
async def _do_verify_finding(_, info, finding_id: str,
                             justification: str) -> SimplePayloadType:
    """Resolve verify_finding mutation."""
    project_name = await \
        sync_to_async(project_domain.get_finding_project_name)(finding_id)
    user_info = util.get_jwt_content(info.context)
    success = await sync_to_async(finding_domain.verify_finding)(
        finding_id, user_info['user_email'],
        justification,
        str.join(' ', [user_info['first_name'], user_info['last_name']])
    )
    if success:
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Verified the '
            f'finding_id: {finding_id}')
    return SimplePayloadType(success=success)


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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Verified a request '
            f'in finding_id: {finding_id}')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Updated description in \
finding {finding_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to update \
            description in finding {finding_id}')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Updated treatment in '
            f'finding {finding_id} succesfully')
        util.forces_trigger_deployment(project_name)
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Attempted to update '
            f'treatment in finding {finding_id}')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Draft {} rejected succesfully'.format(finding_id))
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to reject draft {}'.format(finding_id))
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
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Deleted finding: {finding_id} succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Attempted to delete finding: {finding_id}')
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
async def _do_approve_draft(_, info, draft_id: str) -> ApproveDraftPayloadType:
    """Resolve approve_draft mutation."""
    reviewer_email = util.get_jwt_content(info.context)['user_email']
    project_name = await \
        sync_to_async(project_domain.get_finding_project_name)(draft_id)

    has_vulns = [vuln for vuln in vuln_domain.list_vulnerabilities([draft_id])
                 if cast(List[Dict[str, Any]],
                         vuln['historic_state'])[-1].get('state') != 'DELETED']
    if not has_vulns:
        raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
    success, release_date = await sync_to_async(finding_domain.approve_draft)(
        draft_id, reviewer_email)
    if success:
        util.invalidate_cache(draft_id)
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Approved draft in \
            {project_name} project succesfully')
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to approve \
            draft in {project_name} project')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Created draft in '
            f'{project_name} project succesfully')
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
        await sync_to_async(util.cloudwatch_log)(
            info.context, 'Security: Submitted draft '
            f'{finding_id} succesfully')
    return SimplePayloadType(success=success)
