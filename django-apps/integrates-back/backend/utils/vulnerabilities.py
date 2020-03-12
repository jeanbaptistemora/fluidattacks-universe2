from typing import List, Dict, cast
from backend.exceptions import InvalidRange
from backend.typing import Finding as FindingType


def format_data(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    vuln['current_state'] = cast(List[Dict[str, str]],
                                 vuln.get('historic_state', [{}]))[-1].get('state')
    vuln['treatment'] = ('-' if vuln['current_state'] == 'closed'
                         else str(vuln.get('treatment', ''))).lower().capitalize()

    return vuln


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
