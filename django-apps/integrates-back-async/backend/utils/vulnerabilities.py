from typing import Iterable, List, Dict, Union, cast
import html
import itertools
from operator import itemgetter
import rollbar
from backend.exceptions import InvalidRange
from backend.typing import Finding as FindingType


def format_data(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    vuln['current_state'] = cast(List[Dict[str, str]],
                                 vuln.get('historic_state', [{}]))[-1].get('state')

    return vuln


def as_range(iterable: Iterable) -> str:
    """Convert range into string."""
    my_list = list(iterable)
    range_value = ''
    if len(my_list) > 1:
        range_value = '{0}-{1}'.format(my_list[0], my_list[-1])
    else:
        range_value = '{0}'.format(my_list[0])
    return range_value


def get_ranges(numberlist: List[int]) -> str:
    """Transform list into ranges."""
    range_str = ','.join(as_range(g) for _, g in itertools.groupby(
        numberlist,
        key=lambda n,  # type: ignore
        c=itertools.count(): n - next(c))
    )
    return range_str


def get_specific(value: Dict[str, str]) -> int:
    """Get specific value."""
    return int(value.get('specific', ''))


def sort_vulnerabilities(item: List[str]) -> List[str]:
    """Sort a vulnerability by its where field."""
    sorted_item = sorted(item, key=itemgetter('where'))
    return sorted_item


def group_specific(specific: List[str], vuln_type: str) -> List[Dict[str, FindingType]]:
    """Group vulnerabilities by its specific field."""
    sorted_specific = sort_vulnerabilities(specific)
    lines = []
    vuln_keys = ['historic_state', 'vuln_type', 'UUID', 'finding_id']
    for key, group in itertools.groupby(sorted_specific,
                                        key=lambda x: x['where']):  # type: ignore
        vuln_info = list(group)
        if vuln_type == 'inputs':
            specific_grouped: List[Union[int, str]] = [
                cast(Dict[str, str], i).get('specific', '') for i in vuln_info]
            dictlines: Dict[str, FindingType] = \
                {'where': key, 'specific': ','.join(cast(List[str], specific_grouped))}
        else:
            specific_grouped = [get_specific(cast(Dict[str, str], i)) for i in vuln_info]
            specific_grouped.sort()
            dictlines = {'where': key, 'specific': get_ranges(cast(List[int], specific_grouped))}
        if vuln_info and all(key_vuln in vuln_info[0] for key_vuln in vuln_keys):
            dictlines.update({key_vuln: cast(Dict[str, FindingType], vuln_info[0]).get(key_vuln)
                             for key_vuln in vuln_keys})
        else:
            # Vulnerability doesn't have more attributes.
            pass
        lines.append(dictlines)
    return lines


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


def is_range(specific: str) -> bool:
    """Validate if a specific field has range value."""
    return '-' in specific


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return ',' in specific


def range_to_list(range_value: str) -> List[str]:
    """Convert a range value into list."""
    limits = range_value.split('-')
    if int(limits[1]) > int(limits[0]):
        init_val = int(limits[0])
        end_val = int(limits[1]) + 1
    else:
        error_value = '"values": "{init_val} >= {end_val}"'.format(
            init_val=limits[0],
            end_val=limits[1]
        )
        raise InvalidRange(expr=error_value)
    specific_values = list(map(str, list(range(init_val, end_val))))
    return specific_values


def format_vulnerabilities(
        vulnerabilities: List[Dict[str, FindingType]]) -> \
        Dict[str, List[FindingType]]:
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
        all_states = cast(List[Dict[str, FindingType]], vuln.get('historic_state'))
        current_state = all_states[len(all_states) - 1].get('state')
        vuln_type = str(vuln.get('vuln_type', ''))
        if vuln_type in vulns_types:
            finding[vuln_type].append({
                vuln_values[vuln_type]['where']:
                    html.parser.HTMLParser().unescape(vuln.get('where')),  # type: ignore
                vuln_values[vuln_type]['specific']:
                    html.parser.HTMLParser().unescape(vuln.get('specific')),  # type: ignore
                'state': str(current_state)
            })
        else:
            error_msg = 'Error: Vulnerability {vuln_id} of finding \
                {finding_id} does not have the right type'\
                .format(vuln_id=vuln.get('UUID'), finding_id=vuln.get('finding_id'))
            rollbar.report_message(error_msg, 'error')
    return finding


def format_where(where: str, vulnerabilities: List[Dict[str, str]]) -> str:
    for vuln in vulnerabilities:
        where = '{where!s}{vuln_where!s} ({vuln_specific!s})\n'.format(
            where=where, vuln_where=vuln.get('where'), vuln_specific=vuln.get('specific'))
    return where
