# Standard libraries
import io
import itertools
import logging
import logging.config
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

# Third-party libraries
from aioextensions import (
    in_process,
    schedule,
)
from boto3.dynamodb.conditions import Key
from starlette.datastructures import UploadFile

# Local libraries
from back.settings import LOGGING
from backend import (
    mailer,
    util,
)
from backend.dal import project as group_dal
from backend.dal.helpers import dynamodb
from backend.domain import project as group_domain
from backend.exceptions import (
    InvalidDateFormat,
    InvalidFileStructure,
)
from backend.filters import finding as finding_filters
from backend.typing import (
    Action,
    Datetime,
    Finding as FindingType,
    Historic as HistoricType,
    MailContent as MailContentType,
)
from newutils import (
    cvss,
    datetime as datetime_utils,
    forms as forms_utils,
)
from __init__ import (
    BASE_URL,
    FI_MAIL_REVIEWERS,
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
FINDINGS_TABLE: str = 'FI_findings'
LOGGER = logging.getLogger(__name__)


async def append_records_to_file(
    records: List[Dict[str, str]],
    new_file: UploadFile
) -> UploadFile:
    header = records[0].keys()
    values = [
        list(v)
        for v in [
            record.values()
            for record in records
        ]
    ]
    new_file_records = await new_file.read()
    await new_file.seek(0)
    new_file_header = cast(
        bytes,
        new_file_records
    ).decode('utf-8').split('\n')[0]
    new_file_records = r'\n'.join(
        cast(bytes, new_file_records).decode('utf-8').split('\n')[1:]
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
    uploaded_file = UploadFile(filename=new_file.name)
    await uploaded_file.write(buff.read())
    await uploaded_file.seek(0)
    return uploaded_file


def clean_deleted_state(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    historic_state = cast(
        List[Dict[str, str]],
        vuln.get('historic_state', [])
    )
    new_historic = list(
        filter(
            lambda historic: historic.get('state') != 'DELETED',
            historic_state
        )
    )
    vuln['historic_state'] = new_historic
    return vuln


def filter_by_date(
    historic_items: List[Dict[str, str]],
    cycle_date: Datetime
) -> List[Dict[str, str]]:
    return list(
        filter(
            lambda historic:
                historic.get('date') and get_item_date(historic) <= cycle_date,
            historic_items
        )
    )


# pylint: disable=simplifiable-if-expression
def format_data(finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    finding = {
        util.snakecase_to_camelcase(attribute): finding.get(attribute)
        for attribute in finding
    }

    is_draft = not finding_filters.is_released(finding)
    if is_draft:
        finding['cvssVersion'] = finding.get('cvssVersion', '2')

    if 'cvssVersion' not in finding:
        finding['cvssVersion'] = '3.1'

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
        historic_verification[-1].get('status') == 'REQUESTED' and not
        historic_verification[-1].get('vulns', [])
    )

    finding_files = cast(List[Dict[str, str]], finding.get('files', []))
    finding['evidence'] = {
        'animation': get_evidence('animation', finding_files, finding),
        'evidence1': get_evidence('evidence_route_1', finding_files, finding),
        'evidence2': get_evidence('evidence_route_2', finding_files, finding),
        'evidence3': get_evidence('evidence_route_3', finding_files, finding),
        'evidence4': get_evidence('evidence_route_4', finding_files, finding),
        'evidence5': get_evidence('evidence_route_5', finding_files, finding),
        'exploitation': get_evidence('exploitation', finding_files, finding)
    }
    finding['compromisedAttrs'] = finding.get('records', '')
    finding['records'] = get_evidence('fileRecords', finding_files, finding)
    finding['exploit'] = get_evidence('exploit', finding_files, finding)

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


def format_finding(
    finding: Dict[str, FindingType],
    attrs: Optional[Set[str]] = None
) -> Dict[str, FindingType]:
    """Returns the data in the format expected by default resolvers"""
    formated_finding = finding.copy()
    if not attrs or 'finding_id' in attrs:
        formated_finding['id'] = finding['finding_id']
    if not attrs or 'finding' in attrs:
        formated_finding['title'] = finding['finding']
    if not attrs or 'historic_state' in attrs:
        formated_finding['historic_state'] = finding.get('historic_state', [])
    return formated_finding


def get_date_with_format(item: Dict[str, str]) -> str:
    return str(item.get('date', '')).split(' ')[0]


def get_evidence(
    name: str,
    items: List[Dict[str, str]],
    finding: Dict[str, FindingType],
) -> Dict[str, str]:
    date_str: str = (
        finding_filters.get_approval_date(finding) or
        finding_filters.get_creation_date(finding)
    )
    release_date = datetime_utils.get_from_str(date_str)
    evidence = [
        {
            'date': (
                item['upload_date']
                if datetime_utils.get_from_str(
                    item.get('upload_date', datetime_utils.DEFAULT_STR)
                ) > release_date
                else date_str
            ),
            'description': item.get('description', ''),
            'url': item['file_url']
        }
        for item in items
        if item['name'] == name
    ]
    return evidence[0] if evidence else {'url': '', 'description': ''}


def get_first_historic_item_date(historic: List[Dict[str, str]]) -> str:
    date: str = ''
    if historic:
        date = get_date_with_format(historic[0])
    return date


def get_historic_dates(vuln: Dict[str, FindingType]) -> List[str]:
    historic_treatment = cast(
        List[Dict[str, str]],
        vuln['historic_treatment']
    )
    historic_state = cast(
        List[Dict[str, str]],
        vuln['historic_state']
    )
    treatment_dates = [
        get_date_with_format(treatment)
        for treatment in historic_treatment
    ]
    state_dates = [
        get_date_with_format(state)
        for state in historic_state
        if state.get('state', '') in {'open', 'closed'}
    ]
    return treatment_dates + state_dates


async def get_historic_verification(
    finding_id: str
) -> List[Dict[str, FindingType]]:
    historic_verification: List[Dict[str, FindingType]] = []
    query_attrs = {
        'KeyConditionExpression': Key('finding_id').eq(finding_id),
        'ProjectionExpression': 'historic_verification'
    }
    response_items = cast(
        List[Dict[str, FindingType]],
        await dynamodb.async_query(FINDINGS_TABLE, query_attrs)
    )
    if response_items:
        historic_verification = response_items[0].get(
            'historic_verification',
            []
        )
    return historic_verification


def get_item_date(item: Any) -> Datetime:
    return datetime_utils.get_from_str(item['date'].split(' ')[0], '%Y-%m-%d')


def get_reattack_requesters(
    historic_verification: List[Dict[str, str]],
    vulnerabilities: List[str]
) -> List[str]:
    historic_verification = list(reversed(historic_verification))
    users: List[str] = []
    for verification in historic_verification:
        if verification.get('status', '') == 'REQUESTED':
            vulns = cast(List[str], verification.get('vulns', []))
            if any([vuln for vuln in vulns if vuln in vulnerabilities]):
                vulnerabilities = [
                    vuln for vuln in vulnerabilities if vuln not in vulns
                ]
                users.append(str(verification.get('user', '')))
        if not vulnerabilities:
            break
    return list(set(users))


def get_sorted_historics(
    vuln: Dict[str, FindingType]
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    historic_treatment = cast(
        List[Dict[str, str]],
        vuln.get('historic_treatment', [])
    )
    historic_state = cast(
        List[Dict[str, str]],
        vuln.get('historic_state', [])
    )
    sorted_historic = sort_historic_by_date(historic_state)
    sorted_treatment = sort_historic_by_date(historic_treatment)
    return sorted_historic, sorted_treatment


def get_state_actions(vulns: List[Dict[str, FindingType]]) -> List[Action]:
    states_actions = list(
        itertools.chain.from_iterable(
            get_vuln_state_action(
                sort_historic_by_date(vuln['historic_state'])
            )
            for vuln in vulns
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(states_actions).most_common()
    ]
    return actions


def get_tracking_dates(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[str]:
    """Remove vulnerabilities that changes in the same day."""
    vuln_casted: List[List[str]] = [
        get_historic_dates(vuln)
        for vuln in vulnerabilities
    ]
    new_casted: List[str] = sorted(
        list(
            {
                date
                for dates in vuln_casted
                for date in dates
            }
        )
    )
    return new_casted


def get_treatment_actions(vulns: List[Dict[str, FindingType]]) -> List[Action]:
    treatments_actions = list(
        itertools.chain.from_iterable(
            get_vuln_treatment_actions(
                sort_historic_by_date(vuln['historic_treatment'])
            )
            for vuln in vulns
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(treatments_actions).most_common()
    ]
    return actions


def get_vuln_state_action(historic_state: HistoricType) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=state['state'],
            date=state['date'].split(' ')[0],
            justification='',
            manager='',
            times=1,
        )
        for state in historic_state
    ]
    return list({action.date: action for action in actions}.values())


def get_vuln_treatment_actions(
    historic_treatment: HistoricType
) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=treatment['treatment'],
            date=treatment['date'].split(' ')[0],
            justification=treatment['justification'],
            manager=treatment['treatment_manager'],
            times=1,
        )
        for treatment in historic_treatment
        if (
            treatment['treatment'] in {'ACCEPTED', 'ACCEPTED_UNDEFINED'} and
            treatment.get('acceptance_status') not in {'REJECTED', 'SUBMITTED'}
        )
    ]
    return list({action.date: action for action in actions}.values())


async def send_finding_verified_email(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    finding_name: str,
    group_name: str,
    historic_verification: List[Dict[str, str]],
    vulnerabilities: List[str]
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    all_recipients = await group_domain.get_users_to_notify(group_name)
    recipients = await in_process(
        get_reattack_requesters,
        historic_verification,
        vulnerabilities
    )
    recipients = [
        recipient for recipient in recipients if recipient in all_recipients
    ]
    schedule(
        mailer.send_mail_verified_finding(
            recipients,
            {
                'project': group_name,
                'organization': org_name,
                'finding_name': finding_name,
                'finding_url': (
                    f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                    f'/vulns/{finding_id}/tracking'
                ),
                'finding_id': finding_id
            }
        )
    )


def sort_historic_by_date(historic: Any) -> HistoricType:
    historic_sort = sorted(historic, key=lambda i: i['date'])
    return historic_sort


async def send_draft_reject_mail(  # pylint: disable=too-many-arguments
    context: Any,
    draft_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    reviewer_email: str
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients.append(discoverer_email)
    email_context: MailContentType = {
        'admin_mail': reviewer_email,
        'analyst_mail': discoverer_email,
        'draft_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
            f'/drafts/{draft_id}/description'
        ),
        'finding_id': draft_id,
        'finding_name': finding_name,
        'project': group_name,
        'organization': org_name
    }
    schedule(mailer.send_mail_reject_draft(recipients, email_context))


async def send_finding_delete_mail(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    justification: str
) -> None:
    del context
    recipients = FI_MAIL_REVIEWERS.split(',')

    schedule(
        mailer.send_mail_delete_finding(
            recipients,
            {
                'analyst_email': discoverer_email,
                'finding_name': finding_name,
                'finding_id': finding_id,
                'justification': justification,
                'project': group_name,
            }
        )
    )


async def send_new_draft_mail(
    context: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    analyst_email: str
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients += await group_dal.list_internal_managers(group_name)
    email_context: MailContentType = {
        'analyst_email': analyst_email,
        'finding_id': finding_id,
        'finding_name': finding_title,
        'finding_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
            f'/drafts/{finding_id}/description'
        ),
        'project': group_name,
        'organization': org_name
    }
    schedule(mailer.send_mail_new_draft(recipients, email_context))


def validate_acceptance_date(values: Dict[str, str]) -> bool:
    """
    Check that the date set to temporarily accept a finding is logical
    """
    valid: bool = True
    if values['treatment'] == 'ACCEPTED':
        if values.get("acceptance_date"):
            today = datetime_utils.get_now_as_str()
            values['acceptance_date'] = (
                f'{values["acceptance_date"].split()[0]} {today.split()[1]}'
            )
            if not util.is_valid_format(values['acceptance_date']):
                raise InvalidDateFormat()
        else:
            raise InvalidDateFormat()
    return valid
