import asyncio
import bisect
import io
import itertools
import logging
import threading
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Union, cast, Tuple

import pytz
from asgiref.sync import async_to_sync
from backports import csv
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from magic import Magic
from pytz.tzinfo import DstTzInfo

from backend import mailer, util
from backend.dal import (
    finding as finding_dal,
    project as project_dal
)
from backend.domain import (
    organization as org_domain,
    project as project_domain
)
from backend.exceptions import (
    FindingNotFound,
    InvalidAcceptanceDays,
    InvalidDateFormat,
    InvalidAcceptanceSeverity,
    InvalidFileStructure,
    InvalidNumberAcceptations
)
from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType
)
from backend.utils import (
    aio,
    cvss,
    forms as forms_utils
)
from fluidintegrates.settings import LOGGING
from __init__ import (
    BASE_URL,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS
)

logging.config.dictConfig(LOGGING)

# Constants
CVSS_PARAMETERS = {
    '2': {
        'bs_factor_1': 0.6, 'bs_factor_2': 0.4, 'bs_factor_3': 1.5,
        'impact_factor': 10.41, 'exploitability_factor': 20
    },
    '3.1': {
        'impact_factor_1': 6.42, 'impact_factor_2': 7.52,
        'impact_factor_3': 0.029, 'impact_factor_4': 3.25,
        'impact_factor_5': 0.02, 'impact_factor_6': 15,
        'exploitability_factor_1': 8.22, 'basescore_factor': 1.08,
        'mod_impact_factor_1': 0.915, 'mod_impact_factor_2': 6.42,
        'mod_impact_factor_3': 7.52, 'mod_impact_factor_4': 0.029,
        'mod_impact_factor_5': 3.25, 'mod_impact_factor_6': 0.02,
        'mod_impact_factor_7': 13, 'mod_impact_factor_8': 0.9731
    }
}
LOGGER = logging.getLogger(__name__)


def _get_evidence(name: str, items: List[Dict[str, str]]) -> Dict[str, str]:
    evidence = [
        {'url': item['file_url'],
         'description': item.get('description', '')}
        for item in items
        if item['name'] == name
    ]

    return evidence[0] if evidence else {'url': '', 'description': ''}


async def _download_evidence_file(
        project_name: str,
        finding_id: str,
        file_name: str) -> str:
    file_id = '/'.join([project_name.lower(), finding_id, file_name])
    file_exists = await finding_dal.search_evidence(file_id)

    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = '/tmp' + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)
        await finding_dal.download_evidence(file_id, tmp_filepath)
        return tmp_filepath
    raise Exception('Evidence not found')


def append_records_to_file(
        records: List[Dict[str, str]],
        new_file: InMemoryUploadedFile) -> ContentFile:
    header = records[0].keys()
    values = [
        list(v)
        for v in [
            record.values()
            for record in records
        ]
    ]
    new_file_records = new_file.read()
    new_file_header = new_file_records.decode('utf-8').split('\n')[0]
    new_file_records = r'\n'.join(
        new_file_records.decode('utf-8').split('\n')[1:]
    )
    records_str = ''
    for record in values:
        records_str += repr(str(','.join(record)) + '\n').replace('\'', '')
    aux = records_str
    records_str = (
        str(','.join(header)) +
        r'\n' + aux +
        str(new_file_records).replace('\'', '')
    )
    if new_file_header != str(','.join(header)):
        raise InvalidFileStructure()

    buff = io.BytesIO(
        records_str.encode('utf-8').decode('unicode_escape').encode('utf-8')
    )
    content_file: ContentFile = ContentFile(buff.read())
    content_file.close()
    return content_file


def cast_tracking(
    tracking: List[Tuple[str, Dict[str, int]]]
) -> List[Dict[str, Union[int, str]]]:
    """Cast tracking in accordance to schema."""
    cycle = 0
    tracking_casted = []
    for date, value in tracking:
        effectiveness = int(
            (
                int(value['closed']) / float(value['open'] + value['closed'])
            ) * 100
        )
        closing_cicle: Dict[str, Union[int, str]] = {
            'cycle': cycle,
            'open': value['open'],
            'closed': value['closed'],
            'effectiveness': effectiveness,
            'date': date,
        }
        cycle += 1
        tracking_casted.append(closing_cicle)
    return tracking_casted


async def get_attributes(
        finding_id: str,
        attributes: List[str]) -> Dict[str, FindingType]:
    if 'finding_id' not in attributes:
        attributes = [*attributes, 'finding_id']
    response = await finding_dal.get_attributes(finding_id, attributes)
    if not response:
        raise FindingNotFound()
    return response


async def get_records_from_file(
        project_name: str,
        finding_id: str,
        file_name: str) -> List[Dict[object, object]]:
    file_path = await _download_evidence_file(
        project_name,
        finding_id,
        file_name
    )
    file_content = []
    encoding = Magic(mime_encoding=True).from_file(file_path)

    try:
        with io.open(file_path, mode='r', encoding=encoding) as records_file:
            csv_reader = csv.reader(records_file)
            max_rows = 1000
            headers = next(csv_reader)
            file_content = [
                util.list_to_dict(headers, row)
                for row in itertools.islice(csv_reader, max_rows)
            ]
    except (csv.Error, LookupError, UnicodeDecodeError) as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return file_content


async def get_exploit_from_file(
        project_name: str,
        finding_id: str,
        file_name: str) -> str:
    file_path = await _download_evidence_file(
        project_name,
        finding_id,
        file_name
    )
    file_content = ''

    with open(file_path, 'r') as exploit_file:
        file_content = exploit_file.read()

    return file_content


def get_open_verification_dates(
        vulnerabilities: List[Dict[str, FindingType]]) -> List[str]:
    """Get dates when open vulns were verified."""
    verified_open_dates = set()
    historic_open_verified = []
    for vuln in vulnerabilities:
        historic_state = cast(
            List[Dict[str, str]],
            vuln.get('historic_state', [])
        )
        historic_verification = cast(
            List[Dict[str, str]],
            vuln.get('historic_verification', [])
        )
        historic = historic_state + historic_verification
        sorted_historic = sorted(historic, key=lambda i: i['date'])
        for index in range(1, len(sorted_historic)):
            prev_milestone = sorted_historic[index - 1]
            milestone = sorted_historic[index]
            if 'state' not in milestone:
                milestone['state'] = prev_milestone['state']
        historic_open_verified = list(
            filter(
                lambda i: i.get('state', '') == 'open'
                and i.get('status', '') == 'VERIFIED',
                sorted_historic
            )
        )
        verified_open_dates.update([
            str(milestone.get('date', '')).split(' ')[0]
            for milestone in historic_open_verified
        ])
    return list(verified_open_dates)


def add_open_verification_dates(
    tracking_grouped: Dict[str, Dict[str, int]],
    open_verification_dates: List[str]
) -> List[Tuple[str, Dict[str, int]]]:
    """Add dates to tracking when open vulns were verified."""
    open_verification_tracking = sorted(tracking_grouped.items())
    tracking_dates = [
        date
        for date, _ in open_verification_tracking
    ]
    new_dates = [
        date
        for date in open_verification_dates
        if date not in tracking_dates
    ]
    for new_date in new_dates:
        index = bisect.bisect(tracking_dates, new_date)
        _, value = open_verification_tracking[index - 1]
        new_item = (new_date, value)
        tracking_dates.insert(index, new_date)
        open_verification_tracking.insert(index, new_item)
    return open_verification_tracking


def get_tracking_dict(unique_dict: Dict[str, Dict[str, str]]) -> \
        Dict[str, Dict[str, str]]:
    """Get tracking dictionary."""
    sorted_dates = sorted(unique_dict.keys())
    tracking_dict = {}
    if sorted_dates:
        tracking_dict[sorted_dates[0]] = unique_dict[sorted_dates[0]]
        for date in range(1, len(sorted_dates)):
            prev_date = sorted_dates[date - 1]
            tracking_dict[sorted_dates[date]] = tracking_dict[prev_date].copy()
            actual_date_dict = list(unique_dict[sorted_dates[date]].items())
            for vuln, state in actual_date_dict:
                tracking_dict[sorted_dates[date]][vuln] = state
    return tracking_dict


def get_unique_dict(list_dict: List[Dict[str, Dict[str, str]]]) -> \
        Dict[str, Dict[str, str]]:
    """Get unique dict."""
    unique_dict: Dict[str, Dict[str, str]] = {}
    for entry in list_dict:
        date = next(iter(entry))
        if not unique_dict.get(date):
            unique_dict[date] = {}
        vuln = next(iter(entry[date]))
        unique_dict[date][vuln] = entry[date][vuln]
    return unique_dict


def group_by_state(tracking_dict: Dict[str, Dict[str, str]]) -> \
        Dict[str, Dict[str, int]]:
    """Group vulnerabilities by state."""
    tracking: Dict[str, Dict[str, int]] = {}
    for tracking_date, status in list(tracking_dict.items()):
        for vuln_state in list(status.values()):
            status_dict = tracking.setdefault(
                tracking_date,
                {'open': 0, 'closed': 0}
            )
            status_dict[vuln_state] += 1
    return tracking


# pylint: disable=simplifiable-if-expression
def format_data(finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    finding = {
        util.snakecase_to_camelcase(attribute): finding.get(attribute)
        for attribute in finding
    }

    is_draft = 'releaseDate' not in finding
    if is_draft:
        finding['age'] = 0
        finding['cvssVersion'] = finding.get('cvssVersion', '2')
    else:
        finding['age'] = util.calculate_datediff_since(
            cast(datetime, finding['releaseDate'])
        ).days
    finding['exploitable'] = forms_utils.is_exploitable(
        float(str(finding.get('exploitability', 0))),
        str(finding.get('cvssVersion', ''))
    ) == 'Si'

    historic_verification = cast(
        List[Dict[str, str]],
        finding.get('historicVerification', [{}])
    )
    finding['remediated'] = (
        historic_verification and
        historic_verification[-1].get('status') == 'REQUESTED' and
        not historic_verification[-1].get('vulns', [])
    )

    finding_files = cast(List[Dict[str, str]], finding.get('files', []))
    finding['evidence'] = {
        'animation': _get_evidence('animation', finding_files),
        'evidence1': _get_evidence('evidence_route_1', finding_files),
        'evidence2': _get_evidence('evidence_route_2', finding_files),
        'evidence3': _get_evidence('evidence_route_3', finding_files),
        'evidence4': _get_evidence('evidence_route_4', finding_files),
        'evidence5': _get_evidence('evidence_route_5', finding_files),
        'exploitation': _get_evidence('exploitation', finding_files)
    }
    finding['compromisedAttrs'] = finding.get('records', '')
    finding['records'] = _get_evidence('fileRecords', finding_files)
    finding['exploit'] = _get_evidence('exploit', finding_files)

    cvss_fields = {
        '2': [
            'accessComplexity', 'accessVector', 'authentication',
            'availabilityImpact', 'availabilityRequirement',
            'collateralDamagePotential', 'confidenceLevel',
            'confidentialityImpact', 'confidentialityRequirement',
            'exploitability', 'findingDistribution', 'integrityImpact',
            'integrityRequirement', 'resolutionLevel'
        ],
        '3.1': [
            'attackComplexity', 'attackVector', 'availabilityImpact',
            'availabilityRequirement', 'confidentialityImpact',
            'confidentialityRequirement', 'exploitability',
            'integrityImpact', 'integrityRequirement',
            'modifiedAttackComplexity', 'modifiedAttackVector',
            'modifiedAvailabilityImpact', 'modifiedConfidentialityImpact',
            'modifiedIntegrityImpact', 'modifiedPrivilegesRequired',
            'modifiedUserInteraction', 'modifiedSeverityScope',
            'privilegesRequired', 'remediationLevel', 'reportConfidence',
            'severityScope', 'userInteraction'
        ]
    }
    finding['severity'] = {
        field: cast(str, float(str(finding.get(field, 0))))
        for field in cvss_fields[str(finding['cvssVersion'])]
    }
    base_score = cvss.calculate_cvss_basescore(
        cast(Dict[str, float], finding['severity']),
        CVSS_PARAMETERS[str(finding['cvssVersion'])],
        str(finding['cvssVersion'])
    )
    finding['severityCvss'] = cvss.calculate_cvss_temporal(
        cast(Dict[str, float], finding['severity']),
        base_score,
        str(finding['cvssVersion'])
    )

    return finding


async def mask_treatment(
        finding_id: str,
        historic_treatment: List[Dict[str, str]]) -> bool:
    historic = [
        {**treatment, 'user': 'Masked', 'justification': 'Masked'}
        for treatment in historic_treatment
    ]
    return await finding_dal.update(
        finding_id,
        {'historic_treatment': historic}
    )


async def mask_verification(
        finding_id: str,
        historic_verification: List[Dict[str, str]]) -> bool:
    historic = [
        {**treatment, 'user': 'Masked'}
        for treatment in historic_verification
    ]
    return await finding_dal.update(
        finding_id,
        {'historic_verification': historic}
    )


def send_finding_verified_email(
        finding_id: str,
        finding_name: str,
        project_name: str) -> None:
    recipients = async_to_sync(project_domain.get_users_to_notify)(
        project_name
    )

    email_send_thread = threading.Thread(
        name='Verified finding email thread',
        target=mailer.send_mail_verified_finding,
        args=(recipients, {
            'project': project_name,
            'finding_name': finding_name,
            'finding_url': (
                f'{BASE_URL}/groups/{project_name}'
                f'/vulns/{finding_id}/tracking'
            ),
            'finding_id': finding_id
        }))

    email_send_thread.start()


def remove_repeated(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[Dict[str, Dict[str, str]]]:
    """Remove vulnerabilities that changes in the same day."""
    vuln_casted = []
    for vuln in vulnerabilities:
        for state in cast(List[Dict[str, str]], vuln['historic_state']):
            vuln_without_repeated = {}
            format_date = str(state.get('date', '')).split(' ')[0]
            vuln_without_repeated[format_date] = {
                str(vuln['UUID']): str(state.get('state', ''))
            }
            if state.get('approval_status') != 'PENDING':
                vuln_casted.append(vuln_without_repeated)
            else:
                # don't append pending's state to tracking
                pass
    return vuln_casted


def send_finding_delete_mail(
        finding_id: str,
        finding_name: str,
        project_name: str,
        discoverer_email: str,
        justification: str) -> None:
    recipients = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients.extend(approvers)

    email_send_thread = threading.Thread(
        name='Delete finding email thread',
        target=mailer.send_mail_delete_finding,
        args=(recipients, {
            'mail_analista': discoverer_email,
            'name_finding': finding_name,
            'id_finding': finding_id,
            'description': justification,
            'project': project_name,
        }))
    email_send_thread.start()


def send_remediation_email(
        user_email: str,
        finding_id: str,
        finding_name: str,
        project_name: str,
        justification: str) -> None:
    recipients = async_to_sync(project_domain.get_users_to_notify)(
        project_name
    )
    email_send_thread = threading.Thread(
        name='Remediate finding email thread',
        target=mailer.send_mail_remediate_finding,
        args=(recipients, {
            'project': project_name.lower(),
            'finding_name': finding_name,
            'finding_url': (
                f'{BASE_URL}/groups/{project_name}'
                f'/{finding_id}/description'
            ),
            'finding_id': finding_id,
            'user_email': user_email,
            'solution_description': justification
        }))

    email_send_thread.start()


def send_accepted_email(
        finding: Dict[str, FindingType],
        justification: str) -> None:
    project_name = str(finding.get('projectName', ''))
    finding_name = str(finding.get('finding', ''))
    last_historic_treatment = cast(
        List[Dict[str, str]],
        finding.get('historicTreatment')
    )[-1]
    recipients = async_to_sync(project_domain.get_users_to_notify)(
        project_name
    )
    treatment = 'Temporarily accepted'
    if last_historic_treatment['treatment'] == 'ACCEPTED_UNDEFINED':
        treatment = 'Eternally accepted'
    email_send_thread = threading.Thread(
        name='Accepted finding email thread',
        target=mailer.send_mail_accepted_finding,
        args=(recipients, {
            'finding_name': finding_name,
            'finding_id': finding.get('finding_id'),
            'project': project_name.capitalize(),
            'justification': justification,
            'user_email': last_historic_treatment['user'],
            'treatment': treatment
        }))

    email_send_thread.start()


def send_draft_reject_mail(
        draft_id: str,
        project_name: str,
        discoverer_email: str,
        finding_name: str,
        reviewer_email: str) -> None:
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients.append(discoverer_email)
    email_context = {
        'admin_mail': reviewer_email,
        'analyst_mail': discoverer_email,
        'draft_url': (
            f'{BASE_URL}/groups/{project_name}'
            f'/drafts/{draft_id}/description'
        ),
        'finding_id': draft_id,
        'finding_name': finding_name,
        'project': project_name
    }
    email_send_thread = threading.Thread(
        name='Reject draft email thread',
        target=mailer.send_mail_reject_draft,
        args=(recipients, email_context)
    )

    email_send_thread.start()


async def send_new_draft_mail(
        analyst_email: str,
        finding_id: str, finding_title: str,
        project_name: str) -> None:
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients += await project_dal.list_internal_managers(project_name)

    email_context = {
        'analyst_email': analyst_email,
        'finding_id': finding_id,
        'finding_name': finding_title,
        'finding_url': (
            f'{BASE_URL}/groups/{project_name}'
            f'/drafts/{finding_id}/description'
        ),
        'project': project_name
    }
    email_send_thread = threading.Thread(
        name='New draft email thread',
        target=mailer.send_mail_new_draft,
        args=(recipients, email_context))
    email_send_thread.start()


def should_send_mail(
        finding: Dict[str, FindingType],
        updated_values: Dict[str, str]) -> None:
    if updated_values['treatment'] == 'ACCEPTED':
        send_accepted_email(
            finding, str(updated_values.get('justification', ''))
        )
    if updated_values['treatment'] == 'ACCEPTED_UNDEFINED':
        send_accepted_email(
            finding,
            ('Treatment state approval is pending '
             f'for finding {finding.get("finding", "")}')
        )


def validate_acceptance_date(values: Dict[str, str]) -> bool:
    """
    Check that the date set to temporarily accept a finding is logical
    """
    valid: bool = True
    if values['treatment'] == 'ACCEPTED':
        if values.get("acceptance_date"):
            tzn: DstTzInfo = pytz.timezone(settings.TIME_ZONE)
            today = datetime.now(tz=tzn).strftime('%Y-%m-%d %H:%M:%S')
            values['acceptance_date'] = (
                f'{values["acceptance_date"].split()[0]} {today.split()[1]}'
            )
            if not util.is_valid_format(values['acceptance_date']):
                raise InvalidDateFormat()
        else:
            raise InvalidDateFormat()
    return valid


async def validate_acceptance_days(
    values: Dict[str, str],
    organization: str
) -> bool:
    """
    Check that the date during which the finding will be temporarily accepted
    complies with organization settings
    """
    valid: bool = True
    is_valid_acceptance_date = await aio.ensure_io_bound(
        validate_acceptance_date,
        values
    )
    if values.get('treatment') == 'ACCEPTED' and is_valid_acceptance_date:
        tzn: DstTzInfo = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn)
        acceptance_date = datetime.strptime(
            values['acceptance_date'],
            '%Y-%m-%d %H:%M:%S'
        ).replace(tzinfo=tzn)
        acceptance_days = Decimal((acceptance_date - today).days)
        max_acceptance_days = await org_domain.get_max_acceptance_days(
            organization
        )
        if (max_acceptance_days and acceptance_days > max_acceptance_days) or \
                acceptance_days < 0:
            raise InvalidAcceptanceDays(
                'Chosen date is either in the past or exceeds '
                'the maximum number of days allowed by the organization'
            )
    return valid


async def validate_acceptance_severity(
    values: Dict[str, str],
    severity: float,
    organization_id: str
) -> bool:
    """
    Check that the severity of the finding to temporaryly accept is inside
    the range set by the organization
    """
    valid: bool = True
    if values.get('treatment') == 'ACCEPTED':
        current_limits: List[Decimal] = await asyncio.gather(*[
            asyncio.create_task(
                func(organization_id)
            )
            for func in [
                org_domain.get_min_acceptance_severity,
                org_domain.get_max_acceptance_severity
            ]
        ])
        if not (current_limits[0] <=
                Decimal(severity).quantize(Decimal('0.1')) <=
                current_limits[1]):
            raise InvalidAcceptanceSeverity(str(severity))
    return valid


async def validate_number_acceptations(
    values: Dict[str, str],
    historic_treatment: HistoricType,
    organization_id: str
) -> bool:
    """
    Check that a finding to temporarily accept does not exceed the maximum
    number of acceptations the organization set
    """
    valid: bool = True
    if values['treatment'] == 'ACCEPTED':
        max_acceptations = await org_domain.get_max_number_acceptations(
            organization_id
        )
        current_acceptations: int = sum(
            1 for item in historic_treatment if item['treatment'] == 'ACCEPTED'
        )
        if max_acceptations and current_acceptations + 1 > max_acceptations:
            raise InvalidNumberAcceptations(cast(str, current_acceptations))
    return valid


async def validate_treatment_change(
    info_to_check: Dict[str, Union[float, HistoricType, str]],
    organization: str,
    values: Dict[str, str],
) -> bool:
    validate_acceptance_days_task = asyncio.create_task(
        validate_acceptance_days(values, organization)
    )
    validate_acceptance_severity_task = asyncio.create_task(
        validate_acceptance_severity(
            values,
            cast(float, info_to_check['severity']),
            organization
        )
    )
    validate_number_acceptations_task = asyncio.create_task(
        validate_number_acceptations(
            values,
            cast(HistoricType, info_to_check['historic_treatment']),
            organization
        )
    )
    return all(
        await asyncio.gather(
            validate_acceptance_days_task,
            validate_acceptance_severity_task,
            validate_number_acceptations_task
        )
    )
