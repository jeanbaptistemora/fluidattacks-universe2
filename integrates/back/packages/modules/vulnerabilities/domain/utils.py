# Standard library
from typing import (
    cast,
    Dict,
)

# Local
from backend import authz
from backend.exceptions import (
    AcceptionNotRequested,
    InvalidTreatmentManager,
)
from backend.typing import (
    Finding,
    Historic,
)


def compare_historic_treatments(
    last_state: Dict[str, str],
    new_state: Dict[str, str]
) -> bool:
    excluded_attrs = {'acceptance_date', 'acceptance_status', 'date', 'user'}
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
    return (
        (sorted(last_values) != sorted(new_values)) or
        date_change
    )


def validate_acceptation(vuln: Dict[str, Finding]) -> Dict[str, Finding]:
    historic_treatment = cast(
        Historic,
        vuln.get('historic_treatment', [{}])
    )
    if historic_treatment[-1].get('acceptance_status') != 'SUBMITTED':
        raise AcceptionNotRequested()
    return vuln


async def validate_treatment_manager(
    *,
    treatment_manager: str,
    is_customer_admin: bool,
    user_email: str,
    group_name: str,
) -> str:
    if not is_customer_admin:
        treatment_manager = user_email
    enforcer = await authz.get_group_level_enforcer(treatment_manager)
    if not enforcer(group_name, 'valid_treatment_manager'):
        raise InvalidTreatmentManager()
    return treatment_manager
