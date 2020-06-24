from decimal import Decimal
from typing import cast, Dict, Optional

from backend.dal import organization as org_dal


async def get_max_acceptance_days(organization_id: str) -> Optional[Decimal]:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['max_acceptance_days'])
    )
    return result.get('max_acceptance_days', None)


async def get_max_acceptance_severity(organization_id: str) -> Decimal:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['max_acceptance_severity'])
    )
    return result.get('max_acceptance_severity', Decimal('10.0'))


async def get_max_number_acceptations(organization_id: str) -> Optional[Decimal]:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['max_number_acceptations'])
    )
    return result.get('max_number_acceptations', None)


async def get_min_acceptance_severity(organization_id: str) -> Decimal:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['min_acceptance_severity'])
    )
    return result.get('min_acceptance_severity', Decimal('0.0'))
