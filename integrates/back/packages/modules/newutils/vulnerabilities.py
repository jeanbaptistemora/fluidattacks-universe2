# Standard libraries
import html
import itertools
import logging
from datetime import (
    date as datetype,
    datetime,
)
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
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.exceptions import InvalidRange
from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType,
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
VULNS_TABLE: str = 'FI_vulnerabilities'


def as_range(iterable: Iterable[Any]) -> str:
    """Convert range into string."""
    my_list = list(iterable)
    range_value = ''
    if len(my_list) > 1:
        range_value = f'{my_list[0]}-{my_list[-1]}'
    else:
        range_value = f'{my_list[0]}'
    return range_value


async def delete_vulnerability(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    vuln_id: str,
    justification: str,
    user_email: str,
    source: str,
    include_closed_vuln: bool = False
) -> bool:
    vulnerability_loader = context.vulnerability
    vulnerability = await vulnerability_loader.load(vuln_id)
    success = False
    if vulnerability and vulnerability['historic_state']:
        all_states = cast(
            List[Dict[str, str]],
            vulnerability['historic_state']
        )
        current_state = all_states[-1].get('state')
        if current_state == 'open' or include_closed_vuln:
            current_day = datetime_utils.get_now_as_str()
            new_state = {
                'analyst': user_email,
                'date': current_day,
                'justification': justification,
                'source': source,
                'state': 'DELETED',
            }
            all_states.append(new_state)
            success = await update(
                finding_id,
                str(vulnerability['id']),
                {'historic_state': all_states}
            )
    return success


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


def get_specific(value: Dict[str, str]) -> int:
    """Get specific value."""
    return int(value.get('specific', ''))


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


def is_range(specific: str) -> bool:
    """Validate if a specific field has range value."""
    return '-' in specific


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return ',' in specific


def is_vulnerability_closed(vuln: Dict[str, FindingType]) -> bool:
    """Return if a vulnerability is closed."""
    return get_last_status(vuln) == 'closed'


async def mask_vuln(finding_id: str, vuln_id: str) -> bool:
    success = await update(
        finding_id,
        vuln_id,
        {
            'specific': 'Masked',
            'where': 'Masked',
            'treatment_manager': 'Masked',
            'treatment_justification': 'Masked',
        }
    )
    return success


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


async def update(
    finding_id: str,
    vuln_id: str,
    data: Dict[str, FindingType]
) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_names = {}
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'#{attr}, '
            expression_names.update({f'#{attr}': attr})
        else:
            set_expression += f'#{attr} = :{attr}, '
            expression_names.update({f'#{attr}': attr})
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {
            'finding_id': finding_id,
            'UUID': vuln_id,
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    if expression_names:
        update_attrs.update({'ExpressionAttributeNames': expression_names})
    try:
        success = await dynamodb.async_update_item(VULNS_TABLE, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def update_historic_state_dates(
    finding_id: str,
    vuln: Dict[str, FindingType],
    date: str
) -> bool:
    historic_state = cast(HistoricType, vuln['historic_state'])
    for state_info in historic_state:
        state_info['date'] = date
    success = await update(
        finding_id,
        cast(str, vuln['UUID']),
        {'historic_state': historic_state}
    )
    return success
