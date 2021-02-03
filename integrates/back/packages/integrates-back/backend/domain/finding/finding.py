# pylint:disable=too-many-branches
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
    vulnerability as vuln_filters,
)
from backend.utils import (
    comments as comment_utils,
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
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])

    await comment_utils.validate_handle_comment_scope(
        content,
        user_email,
        project_name,
        parent,
        info.context.store
    )

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


async def get_finding_age(
    finding_id: str
) -> int:
    age = 0
    vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    report_dates = vuln_utils.get_report_dates(vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        age = (datetime_utils.get_now() - oldest_report_date).days

    return age


async def get_finding_open_age(
    finding_id: str
) -> int:
    open_age = 0
    vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    open_vulns = vuln_filters.filter_open_vulns(vulns)
    report_dates = vuln_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        open_age = (datetime_utils.get_now() - oldest_report_date).days

    return open_age


async def get_finding_last_vuln_report(
    finding_id: str
) -> int:
    last_vuln_report = 0
    vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
    report_dates = vuln_utils.get_report_dates(vulns)
    if report_dates:
        newest_report_date = max(report_dates)
        last_vuln_report = (datetime_utils.get_now() - newest_report_date).days

    return last_vuln_report


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
    vulns_filtered_zero = filter_zero_risk_vulns(vulns_filtered)
    states_actions = finding_utils.get_state_actions(vulns_filtered_zero)
    treatments_actions = finding_utils.get_treatment_actions(
        vulns_filtered_zero
    )

    tracking_actions = list(
        sorted(
            states_actions + treatments_actions,
            key=lambda action: datetime_utils.get_from_str(
                action.date, '%Y-%m-%d'
            )
        )
    )
    return [
        TrackingItem(
            cycle=index,
            open=action.times if action.action == 'open' else 0,
            closed=action.times if action.action == 'closed' else 0,
            date=action.date,
            accepted=action.times if action.action == 'ACCEPTED' else 0,
            accepted_undefined=(
                action.times if action.action == 'ACCEPTED_UNDEFINED' else 0
            ),
            manager=action.manager,
            justification=action.justification
        )
        for index, action in enumerate(tracking_actions)
    ]


def filter_zero_risk_vulns(
    vulns: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    vulns_filter_non_confirm_zero = vuln_domain.filter_non_confirmed_zero_risk(
        vulns
    )
    vulns_filter_non_request_zero = vuln_domain.filter_non_requested_zero_risk(
        vulns_filter_non_confirm_zero
    )
    return vulns_filter_non_request_zero


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

    if re.match(r'^F[0-9]{3}\. .+',
                str(updated_values.get('finding', ''))):
        return await finding_dal.update(finding_id, updated_values)

    raise InvalidDraftTitle()


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
        analyst = user_info['user_email']
        submission_history.append({
            'state': 'DELETED',
            'date': delete_date,
            'justification': justification,
            'analyst': analyst,
        })
        success = await finding_dal.update(finding_id, {
            'historic_state': submission_history
        })
        schedule(delete_vulnerabilities(finding_id, justification, analyst))

    return success


async def delete_vulnerabilities(
    finding_id: str,
    justification: str,
    user_email: str
) -> bool:
    vulnerabilities = await vuln_domain.list_vulnerabilities_async(
        [finding_id],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )

    return all(await collect(
        vuln_domain.delete_vulnerability(
            finding_id,
            str(vuln['UUID']),
            justification,
            user_email,
            include_closed_vuln=True,
        )
        for vuln in vulnerabilities
    ))


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
