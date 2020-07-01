import sys
from decimal import Decimal
from typing import (
    cast,
    Dict,
    List,
    Optional
)

import rollbar
from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend.dal import organization as org_dal
from backend.exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations
)
from backend.typing import (
    Organization as OrganizationType
)


async def get_id_by_name(organization_name: str) -> str:
    org_id: str = ''
    result: OrganizationType = await org_dal.get_by_name(
        organization_name,
        ['id']
    )
    if result:
        org_id = str(result['id'])
    return org_id


async def get_name_by_id(organization_id: str) -> str:
    org_name: str = ''
    result: OrganizationType = await org_dal.get_by_id(
        organization_id,
        ['name']
    )
    if result:
        org_name = str(result['name'])
    return org_name


async def get_id_for_group(group_name: str) -> str:
    return await org_dal.get_id_for_group(group_name)


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


async def get_max_number_acceptations(organization_id: str) -> \
        Optional[Decimal]:
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


async def update_settings(
    organization_id: str,
    organization_name: str,
    values: OrganizationType
) -> bool:
    """
    Validate setting values to update and update them
    """
    success: bool = False
    valid: List[bool] = []

    values['max_acceptance_severity'] = Decimal(
        cast(
            float,
            values['max_acceptance_severity']
        )
    ).quantize(Decimal('0.1'))
    values['min_acceptance_severity'] = Decimal(
        cast(
            float,
            values['min_acceptance_severity']
        )
    ).quantize(Decimal('0.1'))

    try:
        valid.append(
            validate_acceptance_severity_range(
                cast(Decimal, values['min_acceptance_severity']),
                cast(Decimal, values['max_acceptance_severity'])
            )
        )
        for attr, value in values.items():
            if value is not None:
                validator_func = getattr(
                    sys.modules[__name__],
                    f'validate_{attr}'
                )
                valid.append(validator_func(value))
    except (
        InvalidAcceptanceDays,
        InvalidAcceptanceSeverity,
        InvalidAcceptanceSeverityRange,
        InvalidNumberAcceptations
    ) as exe:
        await sync_to_async(rollbar.report_message)(
            'Invalid values when updating the settings of an organization',
            'error',
            extra_data=exe,
            payload_data=locals()
        )
        raise GraphQLError(str(exe))

    if all(valid):
        success = await org_dal.update(
            organization_id,
            organization_name,
            values
        )
    return success


def validate_acceptance_severity_range(
    min_value: Decimal,
    max_value: Decimal
) -> bool:
    success: bool = True
    if min_value >= max_value:
        raise InvalidAcceptanceSeverityRange()
    return success


def validate_max_acceptance_days(value: int) -> bool:
    success: bool = True
    if value < 0:
        raise InvalidAcceptanceDays()
    return success


def validate_max_acceptance_severity(value: Decimal) -> bool:
    success: bool = True
    if not Decimal('0.0') <= value <= Decimal('10.0'):
        raise InvalidAcceptanceSeverity()
    return success


def validate_max_number_acceptations(value: int) -> bool:
    success: bool = True
    if value < 0:
        raise InvalidNumberAcceptations()
    return success


def validate_min_acceptance_severity(value: Decimal) -> bool:
    success: bool = True
    if not Decimal('0.0') <= value <= Decimal('10.0'):
        raise InvalidAcceptanceSeverity()
    return success
