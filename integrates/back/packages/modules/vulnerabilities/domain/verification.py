
from decimal import Decimal
from typing import (
    Dict,
    cast,
)

from custom_types import (
    Finding,
    Historic,
)
from newutils.vulnerabilities import (
    get_last_status,
    is_reattack_requested,
)


def get_efficacy(vuln: Dict[str, Finding]) -> Decimal:
    cycles: int = get_reattack_cycles(vuln)
    if cycles and get_last_status(vuln) == 'closed':
        return Decimal(100 / cycles).quantize(Decimal('0.01'))
    return Decimal(0)


def get_historic_verification(vuln: Dict[str, Finding]) -> Historic:
    return cast(Historic, vuln.get('historic_verification', []))


def get_last_reattack_date(vuln: Dict[str, Finding]) -> str:
    historic_verification = get_historic_verification(vuln)
    if historic_verification:
        if historic_verification[-1]['status'] == 'VERIFIED':
            return historic_verification[-1]['date']
        if len(historic_verification) >= 2:
            return historic_verification[-2]['date']
    return ''


def get_last_requested_reattack_date(vuln: Dict[str, Finding]) -> str:
    historic_verification = get_historic_verification(vuln)
    if is_reattack_requested(vuln):
        return historic_verification[-1]['date']
    if len(historic_verification) >= 2:
        return historic_verification[-2]['date']
    return ''


def get_reattack_cycles(vuln: Dict[str, Finding]) -> int:
    historic_verification = get_historic_verification(vuln)
    return len([
        verification
        for verification in historic_verification
        if verification['status'] == 'REQUESTED'
    ])
