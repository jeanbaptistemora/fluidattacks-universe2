# Standard libraries
import logging
import logging.config
import re
from contextlib import AsyncExitStack
from decimal import Decimal
from time import time
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

# Third-party libraries
import aioboto3
from aioextensions import (
    collect,
    in_process,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import (
    LOGGING,
    NOEXTRA,
)
from backend import (
    authz,
    mailer,
    util,
)
from backend.exceptions import (
    FindingNotFound,
    InvalidCommentParent,
    InvalidDraftTitle,
    PermissionDenied,
    VulnNotFound,
)
from backend.filters import (
    finding as finding_filters,
    vulnerability as vuln_filters,
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Tracking as TrackingItem,
    Vulnerability as VulnerabilityType,
)
from comments import domain as comments_domain
from dynamodb.operations_legacy import start_context
from findings import dal as findings_dal
from group_access import domain as group_access_domain
from newutils import (
    comments as comments_utils,
    cvss,
    datetime as datetime_utils,
    findings as finding_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from users import domain as users_domain
from vulnerabilities import domain as vulns_domain
from __init__ import BASE_URL


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    finding_id: str,
    group_name: str
) -> bool:
    param_type = comment_data.get('comment_type')
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])

    await comments_utils.validate_handle_comment_scope(
        content,
        user_email,
        group_name,
        parent,
        info.context.store
    )

    if param_type == 'observation':
        enforcer = await authz.get_group_level_enforcer(
            user_email, info.context.store
        )
        if not enforcer(group_name, 'post_finding_observation'):
            raise PermissionDenied()

    if parent != '0':
        finding_comments = [
            str(comment.get('user_id'))
            for comment in await comments_domain.get(
                str(comment_data.get('comment_type')),
                int(finding_id)
            )
        ]
        if parent not in finding_comments:
            raise InvalidCommentParent()

    user_data = await users_domain.get(user_email)
    user_data['user_email'] = user_data.pop('email')
    success = await comments_domain.create(finding_id, comment_data, user_data)
    return success[1]


def cast_new_vulnerabilities(
    finding_new: Dict[str, FindingType],
    finding: Dict[str, FindingType]
) -> Dict[str, FindingType]:
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
        finding['portsVulns'] = vulns_utils.group_specific(
            cast(List[str], finding_new.get('portsVulns')),
            'ports'
        )
        where = vulns_utils.format_where(
            where,
            cast(List[Dict[str, str]], finding['portsVulns'])
        )
    else:
        # This finding does not have ports vulnerabilities
        pass
    if finding_new.get('linesVulns'):
        finding['linesVulns'] = vulns_utils.group_specific(
            cast(List[str], finding_new.get('linesVulns')),
            'lines'
        )
        where = vulns_utils.format_where(
            where,
            cast(List[Dict[str, str]], finding['linesVulns'])
        )
    else:
        # This finding does not have lines vulnerabilities
        pass
    if finding_new.get('inputsVulns'):
        finding['inputsVulns'] = vulns_utils.group_specific(
            cast(List[str], finding_new.get('inputsVulns')),
            'inputs'
        )
        where = vulns_utils.format_where(
            where,
            cast(List[Dict[str, str]], finding['inputsVulns'])
        )
    else:
        # This finding does not have inputs vulnerabilities
        pass
    finding['where'] = where
    return finding


async def delete_finding(
    context: Any,
    finding_id: str,
    justification: str
) -> bool:
    finding_data = await get_finding(finding_id)
    submission_history = cast(
        List[Dict[str, str]],
        finding_data.get('historicState', [{}])
    )
    success = False

    if submission_history[-1].get('state') != 'DELETED':
        delete_date = datetime_utils.get_now_as_str()
        user_info = await util.get_jwt_content(context)
        analyst = user_info['user_email']
        source = util.get_source(context)
        submission_history.append({
            'state': 'DELETED',
            'date': delete_date,
            'justification': justification,
            'analyst': analyst,
            'source': source,
        })
        success = await findings_dal.update(
            finding_id,
            {'historic_state': submission_history}
        )
        schedule(
            delete_vulnerabilities(
                context,
                finding_id,
                justification,
                analyst
            )
        )
    return success


async def delete_vulnerabilities(
    context: Any,
    finding_id: str,
    justification: str,
    user_email: str
) -> bool:
    finding_vulns_loader = context.loaders.finding_vulns
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    source = util.get_source(context)
    return all(
        await collect(
            vulns_domain.delete_vulnerability(
                context.loaders,
                finding_id,
                str(vuln['UUID']),
                justification,
                user_email,
                source,
                include_closed_vuln=True,
            )
            for vuln in vulnerabilities
        )
    )


def filter_zero_risk_vulns(
    vulns: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    vulns_filter_non_confirm_zero = vulns_utils\
        .filter_non_confirmed_zero_risk(vulns)
    vulns_filter_non_request_zero = vulns_utils\
        .filter_non_requested_zero_risk(vulns_filter_non_confirm_zero)
    return vulns_filter_non_request_zero


async def get(
    finding_id: str,
    table: aioboto3.session.Session.client
) -> Dict[str, FindingType]:
    finding = await findings_dal.get(finding_id, table)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()
    return finding_utils.format_data(finding)


async def get_attributes(
    finding_id: str,
    attributes: List[str]
) -> Dict[str, FindingType]:
    if 'finding_id' not in attributes:
        attributes = [*attributes, 'finding_id']
    response = await findings_dal.get_attributes(finding_id, attributes)
    if not response:
        raise FindingNotFound()
    return response


async def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """Retrieves and formats finding attributes"""
    finding = await findings_dal.get_finding(finding_id)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()
    return finding_utils.format_data(finding)


async def get_finding_age(context: Any, finding_id: str) -> int:
    age = 0
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    report_dates = vulns_utils.get_report_dates(vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        age = (datetime_utils.get_now() - oldest_report_date).days
    return age


async def get_finding_last_vuln_report(context: Any, finding_id: str) -> int:
    last_vuln_report = 0
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    report_dates = vulns_utils.get_report_dates(vulns)
    if report_dates:
        newest_report_date = max(report_dates)
        last_vuln_report = (datetime_utils.get_now() - newest_report_date).days
    return last_vuln_report


async def get_finding_open_age(context: Any, finding_id: str) -> int:
    open_age = 0
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    open_vulns = vuln_filters.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        open_age = (datetime_utils.get_now() - oldest_report_date).days
    return open_age


async def get_findings_async(
    finding_ids: List[str]
) -> List[Dict[str, FindingType]]:
    """Retrieves all attributes for the requested findings"""
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(findings_dal.TABLE_NAME)
        findings = await collect(
            get(finding_id, table)
            for finding_id in finding_ids
        )
    return cast(List[Dict[str, FindingType]], findings)


async def get_findings_by_group(
    group_name: str,
    attrs: Optional[Set[str]] = None,
    include_deleted: bool = False
) -> List[Dict[str, FindingType]]:
    if attrs and 'historic_state' not in attrs:
        attrs.add('historic_state')
    findings = await findings_dal.get_findings_by_group(group_name, attrs)
    findings = finding_filters.filter_non_created_findings(findings)
    findings = finding_filters.filter_non_rejected_findings(findings)
    findings = finding_filters.filter_non_submitted_findings(findings)

    if not include_deleted:
        findings = finding_filters.filter_non_deleted_findings(findings)
    return [
        finding_utils.format_finding(finding, attrs)
        for finding in findings
    ]


async def get_last_closing_vuln_info(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, VulnerabilityType]:
    """Get day since last vulnerability closing."""
    finding_vulns_loader = context.finding_vulns_nzr
    validate_findings = await collect(
        validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding
        for finding, is_valid in zip(findings, validate_findings)
        if is_valid
    ]
    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in validated_findings
    ])
    are_vuln_closed = await collect([
        in_process(vulns_utils.is_vulnerability_closed, vuln)
        for vuln in vulns
    ])
    closed_vulns = [
        vuln
        for vuln, is_vuln_closed in zip(vulns, are_vuln_closed)
        if is_vuln_closed
    ]
    closing_vuln_dates = await collect([
        in_process(vulns_utils.get_last_closing_date, vuln)
        for vuln in closed_vulns
    ])
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i)
            for i, v in enumerate(closing_vuln_dates)
        )
        last_closing_vuln = closed_vulns[date_index]
        current_date = max(closing_vuln_dates)
        last_closing_days = (
            Decimal((datetime_utils.get_now().date() - current_date).days)
            .quantize(Decimal('0.1'))
        )
    else:
        last_closing_days = Decimal(0)
        last_closing_vuln = {}
    return last_closing_days, cast(VulnerabilityType, last_closing_vuln)


async def get_group(finding_id: str) -> str:
    attribute = await get_attributes(finding_id, ['project_name'])
    return str(attribute.get('project_name'))


async def get_max_open_severity(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, Dict[str, FindingType]]:
    total_vulns = await collect(
        total_vulnerabilities(context, str(fin.get('finding_id', '')))
        for fin in findings
    )
    opened_findings = [
        finding
        for finding, total_vuln in zip(findings, total_vulns)
        if int(total_vuln.get('openVulnerabilities', '')) > 0
    ]
    total_severity: List[float] = cast(
        List[float],
        [
            finding.get('cvss_temporal', '')
            for finding in opened_findings
        ]
    )
    if total_severity:
        severity, severity_index = max(
            (v, i)
            for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal('0.1'))
        max_severity_finding = opened_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal('0.1'))
        max_severity_finding = {}
    return max_severity, max_severity_finding


async def get_pending_closing_check(context: Any, group: str) -> int:
    """Check for pending closing checks."""
    pending_closing = len(
        await get_pending_verification_findings(context, group)
    )
    return pending_closing


async def get_pending_verification_findings(
    context: Any,
    group_name: str
) -> List[Dict[str, FindingType]]:
    """Gets findings pending for verification"""
    findings_ids = await list_findings(context, [group_name])
    are_pending_verifications = await collect([
        is_pending_verification(context, finding_id)
        for finding_id in findings_ids[0]
    ])
    pending_to_verify_ids = [
        finding_id
        for finding_id, are_pending_verification in zip(
            findings_ids[0],
            are_pending_verifications
        )
        if are_pending_verification
    ]
    pending_to_verify = await collect(
        get_attributes(finding_id, ['finding', 'finding_id', 'project_name'])
        for finding_id in pending_to_verify_ids
    )
    return cast(List[Dict[str, FindingType]], pending_to_verify)


async def get_total_treatment(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    finding_vulns_loader = context.finding_vulns_nzr

    are_findings_valid = await collect(
        validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    valid_findings = [
        finding
        for finding, is_finding_valid in zip(findings, are_findings_valid)
        if is_finding_valid
    ]
    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in valid_findings
    ])

    for vuln in vulns:
        vuln_treatment = cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )[-1].get('treatment')
        current_state = vulns_utils.get_last_status(vuln)
        open_vuln: int = 1 if current_state == 'open' else 0
        if vuln_treatment == 'ACCEPTED':
            accepted_vuln += open_vuln
        elif vuln_treatment == 'ACCEPTED_UNDEFINED':
            indefinitely_accepted_vuln += open_vuln
        elif vuln_treatment == 'IN PROGRESS':
            in_progress_vuln += open_vuln
        else:
            undefined_treatment += open_vuln
    treatment = {
        'accepted': accepted_vuln,
        'acceptedUndefined': indefinitely_accepted_vuln,
        'inProgress': in_progress_vuln,
        'undefined': undefined_treatment
    }
    return treatment


def get_tracking_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[TrackingItem]:
    """get tracking vulnerabilities dictionary"""
    filter_deleted_status = [
        vulns_utils.filter_deleted_status(vuln)
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


def is_deleted(finding: Dict[str, FindingType]) -> bool:
    historic_state = cast(
        List[Dict[str, str]],
        finding.get('historic_state', [{}])
    )
    return historic_state[-1].get('state', '') == 'DELETED'


async def is_pending_verification(context: Any, finding_id: str) -> bool:
    finding_loader = context.finding_vulns_nzr
    vulns = await finding_loader.load(finding_id)
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


async def list_findings(
    context: Any,
    group_names: List[str],
    include_deleted: bool = False
) -> List[List[str]]:
    """Returns a list of the list of finding ids associated with the groups"""
    group_findings_loader = (
        context.group_findings_all
        if include_deleted
        else context.group_findings
    )
    findings = await group_findings_loader.load_many(group_names)
    findings = [
        list(
            map(
                lambda finding: finding['finding_id'],
                group_findings
            )
        )
        for group_findings in findings
    ]
    return cast(List[List[str]], findings)


async def mask_finding(context: Any, finding_id: str) -> bool:
    finding = await findings_dal.get_finding(finding_id)
    finding = finding_utils.format_data(finding)
    historic_verification = cast(
        List[Dict[str, str]],
        finding.get('historicVerification', [])
    )

    attrs_to_mask = [
        'affected_systems',
        'attack_vector_desc',
        'effect_solution',
        'related_findings',
        'risk',
        'threat',
        'treatment',
        'treatment_manager',
        'vulnerability',
        'records'
    ]
    mask_finding_coroutines = []
    mask_finding_coroutines.append(
        findings_dal.update(
            finding_id,
            {attr: 'Masked' for attr in attrs_to_mask}
        )
    )
    mask_finding_coroutines.append(
        mask_verification(finding_id, historic_verification)
    )

    list_evidences_files = await findings_dal.search_evidence(
        f'{finding["projectName"]}/{finding_id}'
    )
    evidence_s3_coroutines = [
        findings_dal.remove_evidence(file_name)
        for file_name in list_evidences_files
    ]
    mask_finding_coroutines.extend(evidence_s3_coroutines)

    evidence_dynamodb_coroutine = findings_dal.update(
        finding_id,
        {
            'files': [
                {
                    'file_url': 'Masked',
                    'name': 'Masked',
                    'description': 'Masked'
                }
                for _ in cast(List[Dict[str, str]], finding['evidence'])
            ]
        }
    )
    mask_finding_coroutines.append(evidence_dynamodb_coroutine)

    comments_and_observations = (
        await comments_domain.get('comment', int(finding_id)) +
        await comments_domain.get('observation', int(finding_id))
    )
    comments_coroutines = [
        comments_domain.delete(int(finding_id), cast(int, comment['user_id']))
        for comment in comments_and_observations
    ]
    mask_finding_coroutines.extend(comments_coroutines)

    finding_all_vulns_loader = context.finding_vulns_all
    vulns = await finding_all_vulns_loader.load(finding_id)
    mask_vulns_coroutines = [
        vulns_domain.mask_vuln(finding_id, str(vuln['UUID']))
        for vuln in vulns
    ]
    mask_finding_coroutines.extend(mask_vulns_coroutines)
    return all(await collect(mask_finding_coroutines))


async def mask_verification(
    finding_id: str,
    historic_verification: List[Dict[str, str]]
) -> bool:
    historic = [
        {
            **treatment,
            'status': 'Masked',
            'user': 'Masked'
        }
        for treatment in historic_verification
    ]
    return await findings_dal.update(
        finding_id,
        {'historic_verification': historic}
    )


async def request_vulnerability_verification(
    context: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str]
) -> bool:
    finding = await findings_dal.get_finding(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_uuids(
        finding_id,
        set(vuln_ids)
    )
    vulnerabilities = [
        vulns_utils.validate_requested_verification(vuln)
        for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get('historic_verification', [])
    )
    historic_verification.append({
        'comment': comment_id,
        'date': today,
        'status': 'REQUESTED',
        'user': user_email,
        'vulns': vuln_ids
    })
    update_finding = await findings_dal.update(
        finding_id,
        {'historic_verification': historic_verification}
    )
    comment_data = {
        'comment_type': 'verification',
        'content': justification,
        'parent': 0,
        'user_id': comment_id
    }
    await comments_domain.create(int(finding_id), comment_data, user_info)

    update_vulns = await collect(
        map(vulns_domain.request_verification, vulnerabilities)
    )
    if all(update_vulns) and update_finding:
        schedule(
            send_remediation_email(
                context,
                user_email,
                finding_id,
                str(finding.get('finding', '')),
                str(finding.get('project_name', '')),
                justification
            )
        )
    else:
        LOGGER.error('An error occurred remediating', **NOEXTRA)
    return all(update_vulns)


async def save_severity(finding: Dict[str, FindingType]) -> bool:
    """Organize severity metrics to save in dynamo."""
    cvss_version: str = str(finding.get('cvssVersion', ''))
    cvss_parameters = finding_utils.CVSS_PARAMETERS[cvss_version]
    severity = cvss.calculate_severity(cvss_version, finding, cvss_parameters)
    response = await findings_dal.update(str(finding.get('id', '')), severity)
    return response


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    finding: Dict[str, FindingType]
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
    context: Any,
    send_email_function: Callable,
    finding_id: str,
    *mail_params: Union[str, Dict[str, str]]
) -> None:
    schedule(send_email_function(context, finding_id, *mail_params))


async def send_remediation_email(  # pylint: disable=too-many-arguments
    context: Any,
    user_email: str,
    finding_id: str,
    finding_name: str,
    group_name: str,
    justification: str
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    recipients = await group_access_domain.get_closers(group_name)
    schedule(
        mailer.send_mail_remediate_finding(
            recipients,
            {
                'project': group_name.lower(),
                'organization': org_name,
                'finding_name': finding_name,
                'finding_url': (
                    f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                    f'/vulns/{finding_id}/locations'
                ),
                'finding_id': finding_id,
                'user_email': user_email,
                'solution_description': justification
            }
        )
    )


async def total_vulnerabilities(
    context: Any,
    finding_id: str
) -> Dict[str, int]:
    finding = {
        'openVulnerabilities': 0,
        'closedVulnerabilities': 0
    }
    finding_vulns_loader = context.finding_vulns
    if await validate_finding(finding_id):
        vulnerabilities = await finding_vulns_loader.load(finding_id)
        last_approved_status = await collect([
            in_process(vulns_utils.get_last_status, vuln)
            for vuln in vulnerabilities
        ])
        for current_state in last_approved_status:
            if current_state == 'open':
                finding['openVulnerabilities'] += 1
            elif current_state == 'closed':
                finding['closedVulnerabilities'] += 1
            else:
                # Vulnerability does not have a valid state
                pass
    return finding


async def update_description(
    finding_id: str,
    updated_values: Dict[str, FindingType]
) -> bool:
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

    if re.match(
        r'^F[0-9]{3}\. .+',
        str(updated_values.get('finding', ''))
    ):
        return await findings_dal.update(finding_id, updated_values)
    raise InvalidDraftTitle()


async def validate_finding(
    finding_id: Union[str, int] = 0,
    finding: Optional[Dict[str, FindingType]] = None
) -> bool:
    """Validate if a finding is not deleted."""
    if not finding:
        finding = await findings_dal.get_finding(str(finding_id))
    return not is_deleted(finding)


async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    info: GraphQLResolveInfo,
    finding_id: str,
    user_info: Dict[str, str],
    parameters: Dict[str, FindingType],
    vulns_to_close_from_file: List[Dict[str, str]]
) -> bool:
    finding_vulns_loader = info.context.loaders.finding_vulns_all
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    vuln_ids = (
        cast(List[str], parameters.get('open_vulns', [])) +
        cast(List[str], parameters.get('closed_vulns', []))
    )
    vulnerabilities = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln['id'] in vuln_ids
    ]
    vulnerabilities = [
        vulns_utils.validate_verify(vuln)
        for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get('historic_verification', [])
    )
    historic_verification.append({
        'comment': comment_id,
        'date': today,
        'status': 'VERIFIED',
        'user': user_email,
        'vulns': vuln_ids
    })
    update_finding = await findings_dal.update(
        finding_id,
        {'historic_verification': historic_verification}
    )
    comment_data = {
        'comment_type': 'verification',
        'content': parameters.get('justification', ''),
        'parent': 0,
        'user_id': comment_id
    }
    await comments_domain.create(int(finding_id), comment_data, user_info)

    success = await collect(
        map(vulns_domain.verify_vulnerability, vulnerabilities)
    )
    if all(success) and update_finding:
        success = await vulns_domain.verify(
            context=info.context.loaders,
            info=info,
            finding_id=finding_id,
            vulnerabilities=vulnerabilities,
            closed_vulns=cast(List[str], parameters.get('closed_vulns', [])),
            date=today,
            vulns_to_close_from_file=vulns_to_close_from_file
        )
    else:
        LOGGER.error('An error occurred verifying', **NOEXTRA)
    return all(success)
