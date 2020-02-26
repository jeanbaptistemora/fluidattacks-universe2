from typing import Any, Dict


def format_data(vuln: Dict[Any, Any]) -> Dict[Any, Any]:
    vuln['current_state'] = vuln.get('historic_state', [{}])[-1].get('state')
    vuln['treatment'] = ('-' if vuln['current_state'] == 'closed'
                         else vuln.get('treatment', '')).lower().capitalize()

    return vuln
