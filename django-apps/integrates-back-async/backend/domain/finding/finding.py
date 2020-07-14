# pylint:disable=too-many-branches
import asyncio
import re
from datetime import datetime
from contextlib import AsyncExitStack
from typing import Dict, List, Union, cast

import aioboto3
import pytz
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from graphql import GraphQLError
from pytz.tzinfo import DstTzInfo

from backend.domain import (
    comment as comment_domain,
    user as user_domain,
    vulnerability as vuln_domain
)

from backend import authz, mailer, util
from backend.exceptions import (
    FindingNotFound,
    InvalidCommentParent,
    InvalidDraftTitle,
)
from backend.utils import (
    aio,
    cvss,
    validations,
    findings as finding_utils,
    vulnerabilities as vuln_utils
)

from backend.dal.helpers.dynamodb import start_context
from backend.dal import (
    comment as comment_dal,
    finding as finding_dal,
    vulnerability as vuln_dal
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Historic as HistoricType,
)


async def add_comment(
        user_email: str, comment_data: CommentType,
        finding_id: str, is_remediation_comment: bool) -> bool:
    parent = str(comment_data.get('parent'))
    if parent != '0':
        finding_comments = [
            str(comment.get('user_id'))
            for comment in await comment_dal.get_comments(
                str(comment_data.get('comment_type')),
                int(finding_id))
        ]
        if parent not in finding_comments:
            raise InvalidCommentParent()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_data['created'] = current_time
    comment_data['modified'] = current_time

    if not is_remediation_comment:
        await aio.ensure_io_bound(
            mailer.send_comment_mail,
            comment_data,
            'finding',
            user_email,
            str(comment_data.get('comment_type')),
            await get_finding(finding_id)
        )
    user_data = user_domain.get(user_email)
    user_data['user_email'] = user_data.pop('email')
    success = await comment_domain.create(finding_id, comment_data, user_data)
    return success[1]


def get_age_finding(act_finding: Dict[str, FindingType]) -> int:
    """Get days since the vulnerabilities was release"""
    today = datetime.now()
    release_date = str(act_finding['releaseDate']).split(' ')
    age = abs(datetime.strptime(release_date[0], '%Y-%m-%d') - today).days
    return age


async def get_tracking_vulnerabilities(
        vulnerabilities: List[Dict[str, FindingType]]) -> List[Dict[str, int]]:
    """get tracking vulnerabilities dictionary"""
    last_approved_status = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_domain.get_last_approved_status)(
                vuln
            )
        )
        for vuln in vulnerabilities
    ])
    vulns_filtered = [
        vuln for vuln in vulnerabilities
        if cast(
            List[Dict[str, str]],
            vuln['historic_state']
        )[-1].get('approval_status') != 'PENDING' or
        last_approved_status.pop(0)
    ]
    filter_deleted_status = await asyncio.gather(*[
        sync_to_async(vuln_domain.filter_deleted_status)(
            vuln
        )
        for vuln in vulns_filtered
    ])
    vulns_filtered = [
        vuln
        for vuln in vulns_filtered
        if filter_deleted_status.pop(0)
    ]
    vuln_casted = finding_utils.remove_repeated(vulns_filtered)
    open_verification_dates = finding_utils.get_open_verification_dates(
        vulns_filtered
    )
    unique_dict = finding_utils.get_unique_dict(vuln_casted)
    tracking = finding_utils.get_tracking_dict(unique_dict)
    tracking_grouped = finding_utils.group_by_state(tracking)
    open_verification_tracking = finding_utils.add_open_verification_dates(
        tracking_grouped, open_verification_dates
    )
    tracking_casted = finding_utils.cast_tracking(open_verification_tracking)
    return tracking_casted


async def handle_acceptation(
        finding_id: str,
        observations: str,
        user_mail: str,
        response: str) -> bool:
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    new_state = {
        'acceptance_status': response,
        'treatment': 'ACCEPTED_UNDEFINED',
        'justification': observations,
        'user': user_mail,
        'date': today
    }
    findind_attr = await finding_utils.get_attributes(
        finding_id,
        ['historic_treatment']
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        findind_attr.get('historic_treatment', [])
    )
    historic_treatment.append(new_state)
    if response == 'REJECTED':
        historic_treatment.append({'treatment': 'NEW', 'date': today})
    return await finding_dal.update(
        finding_id,
        {'historic_treatment': historic_treatment}
    )


async def update_description(
        finding_id: str, updated_values: Dict[str, FindingType]) -> bool:
    validations.validate_fields(
        list(cast(Dict[str, str], updated_values.values()))
    )
    updated_values['finding'] = updated_values.get('title')
    updated_values['vulnerability'] = updated_values.get('description')
    updated_values['effect_solution'] = updated_values.get('recommendation')
    updated_values['records_number'] = str(
        updated_values.get('records_number')
    )
    updated_values['id'] = finding_id
    del updated_values['title']
    del updated_values['description']
    del updated_values['recommendation']
    updated_values = {
        key: None
        if not value
        else value
        for key, value in updated_values.items()
    }
    updated_values = {
        util.camelcase_to_snakecase(k): updated_values.get(k)
        for k in updated_values
    }

    if re.search(r'^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+',
                 str(updated_values.get('finding', ''))):
        return await finding_dal.update(finding_id, updated_values)

    raise InvalidDraftTitle()


async def update_treatment_in_vuln(
        finding_id: str, updated_values: Dict[str, str]) -> bool:
    new_values = cast(Dict[str, FindingType], {
        'treatment': updated_values.get('treatment', ''),
        'treatment_justification': updated_values.get('justification'),
        'acceptance_date': updated_values.get('acceptance_date'),
    })
    if new_values['treatment'] == 'NEW':
        new_values['treatment_manager'] = None
    vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    for vuln in vulns:
        if not any('treatment_manager' in dicts
                   for dicts in [new_values, vuln]):
            finding = await finding_dal.get_finding(finding_id)
            group: str = cast(str, finding.get('project_name', ''))
            email: str = updated_values.get('user', '')
            treatment: str = cast(str, new_values.get('treatment', ''))
            group_level_role: str = await sync_to_async(
                authz.get_group_level_role
            )(email, group)

            new_values['treatment_manager'] = await sync_to_async(
                vuln_domain.set_treatment_manager
            )(
                treatment,
                email,
                finding,
                group_level_role == 'customeradmin',
                email
            )
            break

    update_treatment_result = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_dal.update)(
                finding_id,
                str(vuln.get('UUID', '')),
                new_values.copy()
            )
        )
        for vuln in vulns
    ])
    resp = all(update_treatment_result)
    return resp


async def update_client_description(
    finding_id: str,
    updated_values: Dict[str, str],
    organization: str,
    info_to_check: Dict[str, Union[float, HistoricType, str]],
    user_mail: str
) -> bool:
    """
    Check that the new treatment values to upload are valid and update them
    """
    last_state = {
        key: value
        for key, value in cast(
            List[Dict[str, str]],
            info_to_check['historic_treatment']
        )[-1].items()
        if key not in ['date', 'user']
    }
    new_state = {
        key: value
        for key, value in updated_values.items()
        if key not in ['acceptance_status', 'bts_url']
    }

    bts_changed: bool = bool(
        updated_values.get('bts_url') and
        updated_values.get('bts_url') != info_to_check.get('bts_url')
    )
    treatment_changed: bool = compare_historic_treatments(
        last_state,
        new_state
    )
    if not any([bts_changed, treatment_changed]):
        raise GraphQLError(
            'Finding treatment cannot be updated with the same values'
        )

    validations.validate_fields(list(updated_values.values()))
    success_treatment, success_external_bts = True, True
    if bts_changed:
        validations.validate_url(updated_values['bts_url'])
        validations.validate_field_length(updated_values['bts_url'], 80)
        success_external_bts = await finding_dal.update(
            finding_id,
            {
                'external_bts': updated_values.get('bts_url', None)
            }
        )
    if treatment_changed:
        updated_values.pop('bts_url', None)
        valid_treatment: bool = await finding_utils.validate_treatment_change(
            info_to_check, organization, updated_values
        )
        if valid_treatment:
            success_treatment = await update_treatment(
                finding_id, updated_values, user_mail
            )
    return success_treatment and success_external_bts


async def update_treatment(
        finding_id: str,
        updated_values: Dict[str, str],
        user_mail: str) -> bool:
    success = False
    tzn: DstTzInfo = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).strftime('%Y-%m-%d %H:%M:%S')
    finding = await get_finding(finding_id)
    historic_treatment = cast(
        List[Dict[str, str]],
        finding.get('historicTreatment', [])
    )
    updated_values = util.update_treatment_values(updated_values)
    new_treatment = updated_values['treatment']
    new_state = {
        'date': today,
        'treatment': new_treatment
    }
    if user_mail:
        new_state['user'] = user_mail
    if new_treatment != 'NEW':
        validations.validate_fields([updated_values['justification']])
        validations.validate_field_length(updated_values['justification'], 200)
        new_state['justification'] = updated_values['justification']
        if new_treatment == 'ACCEPTED':
            new_state['acceptance_date'] = updated_values['acceptance_date']
        if new_treatment == 'ACCEPTED_UNDEFINED':
            new_state['acceptance_status'] = \
                updated_values['acceptance_status']
    if historic_treatment:
        historic_treatment.append(new_state)
    else:
        historic_treatment = [new_state]
    result_update_finding = await finding_dal.update(
        finding_id,
        {'historic_treatment': historic_treatment}
    )
    result_update_vuln = await update_treatment_in_vuln(
        finding_id, historic_treatment[-1])
    if result_update_finding and result_update_vuln:
        await aio.ensure_io_bound(
            finding_utils.should_send_mail,
            finding,
            updated_values
        )
        success = True
    return success


def compare_historic_treatments(
        last_state: Dict[str, str],
        new_state: Dict[str, str]) -> bool:
    excluded_attrs = ['date', 'acceptance_date', 'acceptance_status']
    last_values = [
        value
        for key, value in last_state.items()
        if key not in excluded_attrs
    ]
    new_values = [
        value
        for key, value in new_state.items()
        if key not in excluded_attrs
    ]
    date_change = (
        'acceptance_date' in new_state and
        'acceptance_date' in last_state and
        last_state['acceptance_date'].split(' ')[0] !=
        new_state['acceptance_date'].split(' ')[0]
    )
    return sorted(last_values) != sorted(new_values) or date_change


async def save_severity(finding: Dict[str, FindingType]) -> bool:
    """Organize severity metrics to save in dynamo."""
    cvss_version: str = str(finding.get('cvssVersion', ''))
    cvss_parameters = finding_utils.CVSS_PARAMETERS[cvss_version]
    severity = cvss.calculate_severity(cvss_version, finding, cvss_parameters)
    response = await finding_dal.update(str(finding.get('id', '')), severity)
    return response


async def delete_finding(
        finding_id: str,
        project_name: str,
        justification: str,
        context) -> bool:
    finding_data = await get_finding(finding_id)
    submission_history = cast(
        List[Dict[str, str]],
        finding_data.get('historicState', [{}])
    )
    success = False

    if submission_history[-1].get('state') != 'DELETED':
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        today = datetime.now(tz=tzn).today()
        delete_date = str(today.strftime('%Y-%m-%d %H:%M:%S'))
        submission_history.append({
            'state': 'DELETED',
            'date': delete_date,
            'justification': justification,
            'analyst': util.get_jwt_content(context)['user_email'],
        })
        success = await finding_dal.update(finding_id, {
            'historic_state': submission_history
        })

        if success:
            justification_dict = {
                'DUPLICATED': 'It is duplicated',
                'FALSE_POSITIVE': 'It is a false positive',
                'NOT_REQUIRED': 'Finding not required',
            }
            await aio.ensure_io_bound(
                finding_utils.send_finding_delete_mail,
                finding_id,
                str(finding_data.get('finding', '')),
                project_name,
                str(finding_data.get('analyst', '')),
                justification_dict[justification]
            )

    return success


async def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """Retrieves and formats finding attributes"""
    finding = await finding_dal.get_finding(finding_id)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()

    return finding_utils.format_data(finding)


async def get_project(finding_id: str) -> str:
    attribute = await finding_utils.get_attributes(
        finding_id, ['project_name']
    )

    return str(attribute.get('project_name'))


async def get_findings_async(
        finding_ids: List[str]) -> List[Dict[str, FindingType]]:
    """Retrieves all attributes for the requested findings"""
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(finding_dal.TABLE_NAME)
        findings_tasks = [
            asyncio.create_task(
                get(finding_id, table)
            )
            for finding_id in finding_ids
        ]
        findings = await asyncio.gather(*findings_tasks)
    return findings


async def validate_finding(
        finding_id: Union[str, int] = 0,
        finding: Dict[str, FindingType] = None) -> bool:
    """Validate if a finding is not deleted."""
    if not finding:
        finding = await finding_dal.get_finding(str(finding_id))
    historic_state = cast(
        List[Dict[str, str]],
        finding.get('historic_state', [{}])
    )
    return historic_state[-1].get('state', '') != 'DELETED'


def cast_new_vulnerabilities(
        finding_new: Dict[str, FindingType],
        finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """Cast values for new format."""
    if int(str(finding_new.get('openVulnerabilities'))) >= 0:
        finding['openVulnerabilities'] = str(
            finding_new.get('openVulnerabilities')
        )
    else:
        # This finding does not have open vulnerabilities
        pass
    where = '-'
    if finding_new.get('portsVulns'):
        finding['portsVulns'] = vuln_utils.group_specific(
            cast(
                List[str],
                finding_new.get('portsVulns')
            ),
            'ports'
        )
        where = vuln_utils.format_where(where, cast(
            List[Dict[str, str]],
            finding['portsVulns']
        ))
    else:
        # This finding does not have ports vulnerabilities
        pass
    if finding_new.get('linesVulns'):
        finding['linesVulns'] = vuln_utils.group_specific(
            cast(
                List[str],
                finding_new.get('linesVulns')
            ),
            'lines'
        )
        where = vuln_utils.format_where(where, cast(
            List[Dict[str, str]],
            finding['linesVulns']
        ))
    else:
        # This finding does not have lines vulnerabilities
        pass
    if finding_new.get('inputsVulns'):
        finding['inputsVulns'] = vuln_utils.group_specific(
            cast(
                List[str],
                finding_new.get('inputsVulns')
            ),
            'inputs'
        )
        where = vuln_utils.format_where(where, cast(
            List[Dict[str, str]],
            finding['inputsVulns']
        ))
    else:
        # This finding does not have inputs vulnerabilities
        pass
    finding['where'] = where
    return finding


async def get(
        finding_id: str,
        table: aioboto3.session.Session.client) -> Dict[str, FindingType]:
    finding = await finding_dal.get(finding_id, table)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()

    return finding_utils.format_data(finding)


async def is_pending_verification(finding_id: str) -> bool:
    vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    open_vulns = [
        vuln
        for vuln in vulns
        if cast(
            List[Dict[str, str]],
            vuln.get('historic_state', [{}])
        )[-1].get('state') == 'open'
    ]
    reattack_requested = [
        vuln
        for vuln in open_vulns
        if cast(
            List[Dict[str, str]],
            vuln.get('historic_verification', [{}])
        )[-1].get('status') == 'REQUESTED'
    ]

    return len(reattack_requested) > 0 and await validate_finding(finding_id)


@async_to_sync
async def mask_finding(finding_id: str) -> bool:
    finding = await finding_dal.get_finding(finding_id)
    finding = finding_utils.format_data(finding)
    historic_treatment = cast(
        List[Dict[str, str]],
        finding.get('historicTreatment', [])
    )
    historic_verification = cast(
        List[Dict[str, str]],
        finding.get('historicVerification', [])
    )

    attrs_to_mask = [
        'affected_systems', 'attack_vector_desc', 'effect_solution',
        'related_findings', 'risk', 'threat', 'treatment',
        'treatment_manager', 'vulnerability'
    ]
    mask_finding_tasks = []
    mask_finding_tasks.append(
        asyncio.create_task(
            finding_dal.update(finding_id, {
                attr: 'Masked'
                for attr in attrs_to_mask
            })
        )
    )

    mask_finding_tasks.append(
        asyncio.create_task(
            finding_utils.mask_treatment(finding_id, historic_treatment)
        )
    )

    mask_finding_tasks.append(
        asyncio.create_task(
            finding_utils.mask_verification(finding_id, historic_verification)
        )
    )

    list_evidences_files = await finding_dal.search_evidence(
        f'{finding["projectName"]}/{finding_id}'
    )
    evidence_s3_task = [
        asyncio.create_task(
            finding_dal.remove_evidence(file_name)
        )
        for file_name in list_evidences_files
    ]
    mask_finding_tasks.extend(evidence_s3_task)

    evidence_dynamodb_task = asyncio.create_task(
        finding_dal.update(finding_id, {
            'files': [
                {
                    'file_url': 'Masked',
                    'name': 'Masked',
                    'description': 'Masked'
                }
                for _ in cast(List[Dict[str, str]], finding['evidence'])
            ]
        })
    )
    mask_finding_tasks.append(evidence_dynamodb_task)

    comments_and_observations = (
        await comment_dal.get_comments('comment', int(finding_id)) +
        await comment_dal.get_comments('observation', int(finding_id))
    )
    comments_task = [
        asyncio.create_task(
            comment_dal.delete(int(finding_id), cast(int, comment['user_id']))
        )
        for comment in comments_and_observations
    ]
    mask_finding_tasks.extend(comments_task)

    list_vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    mask_vulns_task = [
        asyncio.create_task(
            sync_to_async(vuln_utils.mask_vuln)(
                finding_id, str(vuln['UUID']))
        )
        for vuln in list_vulns
    ]
    mask_finding_tasks.extend(mask_vulns_task)

    success = all(await asyncio.gather(*mask_finding_tasks))
    util.invalidate_cache(finding_id)

    return success
