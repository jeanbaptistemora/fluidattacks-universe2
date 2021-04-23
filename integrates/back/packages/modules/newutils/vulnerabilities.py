# Standard libraries
import html
import itertools
import logging
from datetime import (
    date as datetype,
    datetime,
)
from decimal import Decimal
from operator import itemgetter
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Union,
)

# Third-party libraries
from aioextensions import (
    collect,
    in_process,
)

# Local libraries
from back.settings import LOGGING
from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType,
)
from custom_exceptions import (
    AlreadyRequested,
    InvalidRange,
    NotVerificationRequested,
    VulnAlreadyClosed,
)
from . import datetime as datetime_utils


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
Treatments = NamedTuple('Treatments', [
    ('ACCEPTED', int),
    ('ACCEPTED_UNDEFINED', int),
    ('IN_PROGRESS', int),
    ('NEW', int),
])


def as_range(iterable: Iterable[Any]) -> str:
    """Convert range into string."""
    my_list = list(iterable)
    range_value = ''
    if len(my_list) > 1:
        range_value = f'{my_list[0]}-{my_list[-1]}'
    else:
        range_value = f'{my_list[0]}'
    return range_value


def filter_deleted_status(vuln: Dict[str, FindingType]) -> bool:
    historic_state = cast(List[Dict[str, str]], vuln['historic_state'])
    if historic_state[-1].get('state') == 'DELETED':
        return False
    return True


def filter_non_confirmed_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(
            HistoricType,
            vulnerability.get('historic_zero_risk', [{}])
        )[-1].get('status', '') != 'CONFIRMED'
    ]


def filter_non_requested_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(
            HistoricType,
            vulnerability.get('historic_zero_risk', [{}])
        )[-1].get('status', '') != 'REQUESTED'
    ]


def format_data(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    vuln['current_state'] = cast(
        List[Dict[str, str]],
        vuln.get('historic_state', [{}])
    )[-1].get('state')
    return vuln


def format_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> Dict[str, List[FindingType]]:
    """Format vulnerabilitites."""
    finding: Dict[str, List[FindingType]] = {
        'ports': [],
        'lines': [],
        'inputs': []
    }
    vulns_types = ['ports', 'lines', 'inputs']
    vuln_values = {
        'ports': {
            'where': 'host',
            'specific': 'port',
        },
        'lines': {
            'where': 'path',
            'specific': 'line'
        },
        'inputs': {
            'where': 'url',
            'specific': 'field'
        }
    }
    for vuln in vulnerabilities:
        all_states = cast(
            List[Dict[str, FindingType]],
            vuln.get('historic_state')
        )
        current_state = all_states[-1].get('state')
        vuln_type = str(vuln.get('vuln_type', ''))
        if vuln_type in vulns_types:
            finding[vuln_type].append({
                vuln_values[vuln_type]['where']: (
                    html.parser.HTMLParser().unescape(  # type: ignore
                        vuln.get('where')
                    )
                ),
                vuln_values[vuln_type]['specific']: (
                    html.parser.HTMLParser().unescape(  # type: ignore
                        vuln.get('specific')
                    )
                ),
                'state': str(current_state)
            })
        else:
            LOGGER.error(
                'Vulnerability does not have the right type',
                extra={
                    'extra': {
                        'vuln_uuid': vuln.get("UUID"),
                        'finding_id': vuln.get("finding_id")
                    }
                })
    return finding


def format_where(where: str, vulnerabilities: List[Dict[str, str]]) -> str:
    for vuln in vulnerabilities:
        where = f'{where}{vuln.get("where")} ({vuln.get("specific")})\n'
    return where


def get_last_approved_state(vuln: Dict[str, FindingType]) -> Dict[str, str]:
    historic_state = cast(HistoricType, vuln.get('historic_state', [{}]))
    return historic_state[-1]


def get_last_closing_date(
    vulnerability: Dict[str, FindingType],
    min_date: Optional[datetype] = None
) -> Optional[datetype]:
    """Get last closing date of a vulnerability."""
    current_state = get_last_approved_state(vulnerability)
    last_closing_date = None
    if current_state and current_state.get('state') == 'closed':
        last_closing_date = datetime_utils.get_from_str(
            current_state.get('date', '').split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()
        if min_date and min_date > last_closing_date:
            return None
    return last_closing_date


def get_last_status(vuln: Dict[str, FindingType]) -> str:
    historic_state = cast(HistoricType, vuln.get('historic_state', [{}]))
    return historic_state[-1].get('state', '')


async def get_mean_remediate_vulnerabilities(
    vulns: List[Dict[str, FindingType]],
    min_date: Optional[datetype] = None
) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    open_vuln_dates = await collect(
        in_process(get_open_vulnerability_date, vuln, min_date)
        for vuln in vulns
    )
    filtered_open_vuln_dates = [
        vuln
        for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect(
        in_process(get_last_closing_date, vuln, min_date)
        for vuln, open_vuln in zip(vulns, open_vuln_dates)
        if open_vuln
    )
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date:
            total_days += int(
                (closed_vuln_date - filtered_open_vuln_dates[index]).days
            )
        else:
            current_day = datetime_utils.get_now().date()
            total_days += int(
                (current_day - filtered_open_vuln_dates[index]).days
            )
    total_vuln = len(filtered_open_vuln_dates)
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))
        ).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


async def get_open_findings(
    finding_vulns: List[List[Dict[str, FindingType]]]
) -> int:
    last_approved_status = await collect(
        in_process(get_last_status, vuln)
        for vulns in finding_vulns
        for vuln in vulns
    )
    open_findings = [
        vulns
        for vulns, last_approved in zip(finding_vulns, last_approved_status)
        if [vuln for vuln in vulns if last_approved == 'open']
    ]
    return len(open_findings)


def get_open_vulnerability_date(
    vulnerability: Dict[str, FindingType],
    min_date: Optional[datetype] = None
) -> Optional[datetype]:
    """Get open vulnerability date of a vulnerability."""
    open_vulnerability_date: Optional[datetype] = None
    all_states = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_state', [{}])
    )
    open_states = [state for state in all_states if state['state'] == 'open']
    if open_states:
        open_vulnerability_date = datetime_utils.get_from_str(
            open_states[-1]['date'].split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()
        if min_date and min_date > open_vulnerability_date:
            open_vulnerability_date = None
    return open_vulnerability_date


def get_ranges(numberlist: List[int]) -> str:
    """Transform list into ranges."""
    range_str = ','.join(
        as_range(g) for _, g in itertools.groupby(
            numberlist,
            key=lambda n,    # type: ignore
            c=itertools.count(): n - next(c)
        )
    )
    return range_str


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
                    vuln
                    for vuln in vulnerabilities
                    if vuln not in vulns
                ]
                users.append(str(verification.get('user', '')))
        if not vulnerabilities:
            break
    return list(set(users))


def get_report_dates(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[datetime]:
    """Get report dates for vulnerabilities."""
    report_dates = [
        datetime_utils.get_from_str(
            cast(HistoricType, vuln['historic_state'])[0]['date']
        )
        for vuln in vulnerabilities
    ]

    return report_dates


def get_specific(value: Dict[str, str]) -> int:
    """Get specific value."""
    return int(value.get('specific', ''))


def get_treatments(
    vulnerabilities: List[Dict[str, FindingType]]
) -> Treatments:
    treatment_counter = Counter([
        vuln['historic_treatment'][-1]['treatment']
        for vuln in vulnerabilities
        if vuln['historic_state'][-1]['state'] == 'open'
    ])
    return Treatments(
        ACCEPTED=treatment_counter['ACCEPTED'],
        ACCEPTED_UNDEFINED=treatment_counter['ACCEPTED_UNDEFINED'],
        IN_PROGRESS=treatment_counter['IN PROGRESS'],
        NEW=treatment_counter['NEW'],
    )


def group_specific(
    specific: List[str],
    vuln_type: str
) -> List[Dict[str, FindingType]]:
    """Group vulnerabilities by its specific field."""
    sorted_specific = sort_vulnerabilities(specific)
    lines = []
    vuln_keys = ['historic_state', 'vuln_type', 'UUID', 'finding_id']
    for key, group in itertools.groupby(
        sorted_specific,
        key=lambda x: x['where']  # type: ignore
    ):
        vuln_info = list(group)
        if vuln_type == 'inputs':
            specific_grouped: List[Union[int, str]] = [
                cast(Dict[str, str], i).get('specific', '')
                for i in vuln_info
            ]
            dictlines: Dict[str, FindingType] = {
                'where': key,
                'specific': ','.join(cast(List[str], specific_grouped))
            }
        else:
            specific_grouped = [
                get_specific(cast(Dict[str, str], i))
                for i in vuln_info
            ]
            specific_grouped.sort()
            dictlines = {
                'where': key,
                'specific': get_ranges(cast(List[int], specific_grouped))
            }
        if (
                vuln_info and
                all(key_vuln in vuln_info[0] for key_vuln in vuln_keys)
        ):
            dictlines.update({
                key_vuln: cast(
                    Dict[str, FindingType],
                    vuln_info[0]
                ).get(key_vuln)
                for key_vuln in vuln_keys
            })
        else:
            # Vulnerability doesn't have more attributes.
            pass
        lines.append(dictlines)
    return lines


def is_accepted_undefined_vulnerability(
    vulnerability: Dict[str, FindingType]
) -> bool:
    historic_treatment = cast(
        HistoricType,
        vulnerability['historic_treatment']
    )
    return (
        historic_treatment[-1]['treatment'] == 'ACCEPTED_UNDEFINED' and
        get_last_status(vulnerability) == 'open'
    )


def is_range(specific: str) -> bool:
    """Validate if a specific field has range value."""
    return '-' in specific


def is_reattack_requested(vuln: Dict[str, FindingType]) -> bool:
    response = False
    historic_verification = vuln.get('historic_verification', [{}])
    if cast(
        List[Dict[str, str]],
        historic_verification
    )[-1].get('status', '') == 'REQUESTED':
        response = True
    return response


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return ',' in specific


def is_vulnerability_closed(vuln: Dict[str, FindingType]) -> bool:
    """Return if a vulnerability is closed."""
    return get_last_status(vuln) == 'closed'


def sort_vulnerabilities(item: List[str]) -> List[str]:
    """Sort a vulnerability by its where field."""
    sorted_item = sorted(item, key=itemgetter('where'))
    return sorted_item


def range_to_list(range_value: str) -> List[str]:
    """Convert a range value into list."""
    limits = range_value.split('-')
    init_val = int(limits[0])
    end_val = int(limits[1]) + 1
    if end_val <= init_val:
        error_value = f'"values": "{init_val} >= {end_val}"'
        raise InvalidRange(expr=error_value)
    specific_values = list(map(str, list(range(init_val, end_val))))
    return specific_values


def ungroup_specific(specific: str) -> List[str]:
    """Ungroup specific value."""
    values = specific.split(',')
    specific_values = []
    for val in values:
        if is_range(val):
            range_list = range_to_list(val)
            specific_values.extend(range_list)
        else:
            specific_values.append(val)
    return specific_values


def validate_closed(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """ Validate vuln closed """
    if cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_state', [{}])
    )[-1].get('state') == 'closed':
        raise VulnAlreadyClosed()
    return vuln


def validate_requested_verification(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """ Validate vuln is not resquested """
    historic_verification = cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_verification', [{}])
    )
    if historic_verification[-1].get('status', '') == 'REQUESTED':
        raise AlreadyRequested()
    return vuln


def validate_verify(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """ Validate vuln is resquested """
    if not is_reattack_requested(vuln):
        raise NotVerificationRequested()
    return vuln
