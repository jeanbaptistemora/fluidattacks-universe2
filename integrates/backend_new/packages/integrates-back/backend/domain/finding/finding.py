# pylint:disable=too-many-branches
from datetime import datetime
import re
from contextlib import AsyncExitStack
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Union
)

from aioextensions import (
    collect,
    schedule,
)
import aioboto3
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo

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
    PermissionDenied
)
from backend.filters import (
    finding as finding_filters,
)
from backend.utils import (
    cvss,
    datetime as datetime_utils,
    findings as finding_utils,
    validations,
    vulnerabilities as vuln_utils
)

from backend.dal.helpers.dynamodb import start_context
from backend.dal import (
    comment as comment_dal,
    finding as finding_dal,
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Historic as HistoricType,
    Vulnerability as VulnerabilityType,
    Tracking as TrackingItem,
)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    finding_id: str,
    project_name: str
) -> bool:
    param_type = comment_data.get('comment_type')
    parent = str(comment_data.get('parent'))

    if param_type == 'observation':
        enforcer = await authz.get_group_level_enforcer(
            user_email, info.context.store
        )
        if not enforcer(project_name, 'post_finding_observation'):
            raise PermissionDenied()

    if parent != '0':
        finding_comments = [
            str(comment.get('user_id'))
            for comment in await comment_dal.get_comments(
                str(comment_data.get('comment_type')),
                int(finding_id))
        ]
        if parent not in finding_comments:
            raise InvalidCommentParent()

    user_data = await user_domain.get(user_email)
    user_data['user_email'] = user_data.pop('email')
    success = await comment_domain.create(finding_id, comment_data, user_data)
    return success[1]


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    finding
) -> None:
    schedule(
        mailer.send_comment_mail(
            comment_data,
            'finding',
            user_email,
            str(comment_data.get('comment_type')),
            finding
        )
    )


def send_finding_mail(
    send_email_function: Callable,
    finding_id: str,
    *mail_params: Union[str, Dict[str, str]]
) -> None:
    schedule(
        send_email_function(
            finding_id,
            *mail_params
        )
    )


def get_age_finding(
    vulnerabilities: List[VulnerabilityType],
    release_date: str = '',
) -> int:
    age: int = 0
    date_format: str = '%Y-%m-%d'
    open_vulns_dates: List[datetime] = [
        datetime_utils.get_from_str(
            cast(
                HistoricType, vuln.get('historic_state', [{}])
            )[-1].get('date', '').split(' ')[0],
            date_format
        )
        for vuln in vulnerabilities
        if cast(
            HistoricType, vuln.get('historic_state', [{}])
        )[-1].get('state', '') == 'open'
    ]

    if open_vulns_dates:
        return util.calculate_datediff_since(sorted(open_vulns_dates)[0]).days

    if release_date:
        return util.calculate_datediff_since(
            datetime_utils.get_from_str(
                release_date.split(' ')[0], date_format
            )
        ).days

    return age


def get_tracking_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[TrackingItem]:
    """get tracking vulnerabilities dictionary"""
    filter_deleted_status = [
        vuln_domain.filter_deleted_status(vuln)
        for vuln in vulnerabilities
    ]
    vulns_filtered = [
        finding_utils.clean_deleted_state(vuln)
        for vuln, filter_deleted in zip(vulnerabilities, filter_deleted_status)
        if filter_deleted
    ]
    vulns_filtered = vuln_domain.filter_non_confirmed_zero_risk(vulns_filtered)
    vulns_filtered = vuln_domain.filter_non_requested_zero_risk(vulns_filtered)
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
    new_tracked = finding_utils.add_treatment_to_tracking(
        tracking_casted, vulnerabilities
    )
    return new_tracked


async def handle_acceptation(
        finding_id: str,
        observations: str,
        user_mail: str,
        response: str) -> bool:
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
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
    vulns = await vuln_domain.list_vulnerabilities_async(
        [finding_id],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    return await update_historic_treatment_in_vuln(
        finding_id, updated_values, vulns
    )


async def update_historic_treatment_in_vuln(
    finding_id: str,
    updated_values: Dict[str, str],
    vulns: List[Dict[str, FindingType]],
) -> bool:

    return all(await collect(
        vuln_domain.add_vuln_treatment(
            finding_id=finding_id,
            updated_values=updated_values,
            vuln=vuln,
            user_email=updated_values.get('user', ''),
            date=updated_values.get('date', datetime_utils.DEFAULT_STR),
        )
        for vuln in vulns
    ))


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
    success: bool = False
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
        if key not in {'acceptance_status'}
    }

    treatment_changed: bool = compare_historic_treatments(
        last_state,
        new_state
    )
    if not treatment_changed:
        raise GraphQLError(
            'Finding treatment cannot be updated with the same values'
        )

    validations.validate_fields(list(updated_values.values()))

    if treatment_changed:
        valid_treatment: bool = await finding_utils.validate_treatment_change(
            info_to_check, organization, updated_values
        )
        if valid_treatment:
            success = await update_treatment(
                finding_id, updated_values, user_mail
            )

    return success


async def update_treatment(
        finding_id: str,
        updated_values: Dict[str, str],
        user_mail: str) -> bool:
    success = False
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
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
    success = result_update_finding and result_update_vuln
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
        justification: str,
        context: Any) -> bool:
    finding_data = await get_finding(finding_id)
    submission_history = cast(
        List[Dict[str, str]],
        finding_data.get('historicState', [{}])
    )
    success = False

    if submission_history[-1].get('state') != 'DELETED':
        delete_date = datetime_utils.get_as_str(
            datetime_utils.get_now()
        )
        user_info = await util.get_jwt_content(context)
        submission_history.append({
            'state': 'DELETED',
            'date': delete_date,
            'justification': justification,
            'analyst': user_info['user_email'],
        })
        success = await finding_dal.update(finding_id, {
            'historic_state': submission_history
        })

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
        findings = await collect(
            get(finding_id, table)
            for finding_id in finding_ids
        )
    return cast(List[Dict[str, FindingType]], findings)


async def validate_finding(
        finding_id: Union[str, int] = 0,
        finding: Optional[Dict[str, FindingType]] = None) -> bool:
    """Validate if a finding is not deleted."""
    if not finding:
        finding = await finding_dal.get_finding(str(finding_id))
    return not is_deleted(finding)


def is_deleted(finding: Dict[str, FindingType]) -> bool:
    historic_state = cast(
        List[Dict[str, str]],
        finding.get('historic_state', [{}])
    )

    return historic_state[-1].get('state', '') == 'DELETED'


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
    historic_state = cast(
        List[Dict[str, str]],
        finding.get('historicState', [])
    )

    attrs_to_mask = [
        'affected_systems', 'attack_vector_desc', 'effect_solution',
        'related_findings', 'risk', 'threat', 'treatment',
        'treatment_manager', 'vulnerability', 'analyst', 'records'
    ]
    mask_finding_coroutines = []
    mask_finding_coroutines.append(
        finding_dal.update(finding_id, {
            attr: 'Masked'
            for attr in attrs_to_mask
        })
    )

    mask_finding_coroutines.append(
        finding_utils.mask_treatment(finding_id, historic_treatment)
    )

    mask_finding_coroutines.append(
        finding_utils.mask_state(finding_id, historic_state)
    )

    mask_finding_coroutines.append(
        finding_utils.mask_verification(finding_id, historic_verification)
    )

    list_evidences_files = await finding_dal.search_evidence(
        f'{finding["projectName"]}/{finding_id}'
    )
    evidence_s3_coroutines = [
        finding_dal.remove_evidence(file_name)
        for file_name in list_evidences_files
    ]
    mask_finding_coroutines.extend(evidence_s3_coroutines)

    evidence_dynamodb_coroutine = finding_dal.update(finding_id, {
        'files': [
            {
                'file_url': 'Masked',
                'name': 'Masked',
                'description': 'Masked'
            }
            for _ in cast(List[Dict[str, str]], finding['evidence'])
        ]
    })
    mask_finding_coroutines.append(evidence_dynamodb_coroutine)

    comments_and_observations = (
        await comment_dal.get_comments('comment', int(finding_id)) +
        await comment_dal.get_comments('observation', int(finding_id))
    )
    comments_coroutines = [
        comment_dal.delete(int(finding_id), cast(int, comment['user_id']))
        for comment in comments_and_observations
    ]
    mask_finding_coroutines.extend(comments_coroutines)

    list_vulns = await vuln_domain.list_vulnerabilities_async(
        [finding_id],
        should_list_deleted=True,
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    mask_vulns_coroutines = [
        vuln_utils.mask_vuln(finding_id, str(vuln['UUID']))
        for vuln in list_vulns
    ]
    mask_finding_coroutines.extend(mask_vulns_coroutines)

    success = all(await collect(mask_finding_coroutines))
    util.queue_cache_invalidation(finding_id)

    return success


async def get_findings_by_group(
    group_name: str,
    attrs: Set[str] = None,
    include_deleted: bool = False
) -> List[Dict[str, FindingType]]:
    if attrs and 'historic_state' not in attrs:
        attrs.add('historic_state')
    findings = await finding_dal.get_findings_by_group(group_name, attrs)
    findings = finding_filters.filter_non_created_findings(findings)
    findings = finding_filters.filter_non_rejected_findings(findings)
    findings = finding_filters.filter_non_submitted_findings(findings)

    if not include_deleted:
        findings = finding_filters.filter_non_deleted_findings(findings)

    return [
        finding_utils.format_finding(finding, attrs)
        for finding in findings
    ]


async def list_findings(
    group_names: List[str],
    include_deleted: bool = False
) -> List[List[str]]:
    """Returns a list of the list of finding ids associated with the groups"""
    attrs = {'finding_id', 'historic_state'}
    findings = await collect(
        get_findings_by_group(
            group_name,
            attrs,
            include_deleted
        )
        for group_name in group_names
    )
    findings = [
        list(map(
            lambda finding: finding['finding_id'],
            group_findings
        ))
        for group_findings in findings
    ]

    return cast(List[List[str]], findings)
