import sys
from decimal import Decimal
from typing import (
    AsyncIterator,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
)

import rollbar
from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend import authz
from backend.dal import organization as org_dal
from backend.domain import project as group_domain
from backend.exceptions import (
    GroupNotInOrganization,
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations,
    InvalidOrganization,
    UserNotInOrganization
)
from backend.typing import (
    Organization as OrganizationType
)
from backend.utils import aio


DEFAULT_MAX_ACCEPTANCE_DAYS = Decimal('180')
DEFAULT_MAX_SEVERITY = Decimal('10.0')
DEFAULT_MIN_SEVERITY = Decimal('0.0')


async def add_user(organization_id: str, email: str, role: str) -> bool:
    user_added = await org_dal.add_user(organization_id, email)
    role_added = await aio.ensure_io_bound(
        authz.grant_organization_level_role,
        email,
        organization_id,
        role
    )
    return user_added and role_added


async def get_groups(organization_id: str) -> Tuple[str, ...]:
    """Return a tuple of group names for the provided organization."""
    return tuple(await org_dal.get_groups(organization_id))


async def get_id_by_name(organization_name: str) -> str:
    result: OrganizationType = await org_dal.get_by_name(
        organization_name.lower(),
        ['id']
    )
    if not result:
        raise InvalidOrganization()
    return str(result['id'])


async def get_name_by_id(organization_id: str) -> str:
    result: OrganizationType = await org_dal.get_by_id(
        organization_id,
        ['name']
    )
    if not result:
        raise InvalidOrganization()
    return str(result['name'])


async def get_id_for_group(group_name: str) -> str:
    return await org_dal.get_id_for_group(group_name)


async def get_max_acceptance_days(organization_id: str) -> Decimal:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['max_acceptance_days'])
    )
    return result.get('max_acceptance_days', DEFAULT_MAX_ACCEPTANCE_DAYS)


async def get_max_acceptance_severity(organization_id: str) -> Decimal:
    result = cast(
        Dict[str, Decimal],
        await org_dal.get_by_id(organization_id, ['max_acceptance_severity'])
    )
    return result.get('max_acceptance_severity', DEFAULT_MAX_SEVERITY)


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
    return result.get('min_acceptance_severity', DEFAULT_MIN_SEVERITY)


async def get_or_create(organization_name: str, email: str) -> str:
    """
    Return an organization, even if it does not exists,
    in which case it will be created
    """
    org_created: bool = False
    org_role: str = 'customer'
    organization_name = organization_name.lower().strip()

    org = await org_dal.get_by_name(organization_name, ['id', 'name'])
    if org:
        has_access = await has_user_access(email, str(org['id']))
    else:
        org = await org_dal.create(organization_name)
        org_created = True
        org_role = 'customeradmin'

    if org_created or not has_access:
        await add_user(str(org['id']), email, org_role)
    return str(org['id'])


async def get_users(organization_id: str) -> List[str]:
    return await org_dal.get_users(organization_id)


async def has_group(group_name: str, organization_id: str) -> bool:
    return await org_dal.has_group(group_name, organization_id)


async def has_user_access(email: str, organization_id: str) -> bool:
    return await org_dal.has_user_access(email, organization_id) \
        or authz.get_organization_level_role(email, organization_id) == 'admin'


async def move_group(
    group_name: str,
    organization_name: str,
    email: str
) -> bool:
    """
    Verify that a request to move a group to another organization is valid
    and process it
    """
    success: bool = False
    old_organization_id = await get_id_for_group(group_name)
    new_organization_id = await get_id_by_name(
        organization_name.lower().strip()
    )

    if old_organization_id == new_organization_id:
        success = True
    else:
        group_name = group_name.lower()
        if not await has_group(group_name, old_organization_id):
            raise GroupNotInOrganization()
        if not await has_user_access(email, new_organization_id):
            raise UserNotInOrganization(organization_name)

        success = (
            await org_dal.add_group(new_organization_id, group_name) and
            await org_dal.remove_group(old_organization_id, group_name) and
            await move_users(group_name, new_organization_id)
        )
    return success


async def move_users(group_name: str, organization_id: str) -> bool:
    success: bool = False
    group_users = await aio.ensure_io_bound(
        group_domain.get_users,
        group_name,
        True
    )
    have_users_access = await aio.materialize(
        has_user_access(user, organization_id) for user in group_users
    )

    success = all(
        await aio.materialize(
            add_user(organization_id, user, 'customer')
            for user in group_users if not have_users_access.pop(0)
        )
    )
    return success


async def remove_user(organization_id: str, email: str) -> bool:
    if not await has_user_access(email, organization_id):
        raise UserNotInOrganization()

    user_removed = await org_dal.remove_user(organization_id, email)
    role_removed = await aio.ensure_io_bound(
        authz.revoke_organization_level_role,
        email,
        organization_id
    )
    return user_removed and role_removed


async def update_policies(
    organization_id: str,
    organization_name: str,
    values: OrganizationType
) -> bool:
    """
    Validate setting values to update and update them
    """
    success: bool = False
    valid: List[bool] = []

    try:
        for attr, value in values.items():
            if value is not None:
                value = (
                    Decimal(value).quantize(Decimal('0.1'))
                    if isinstance(value, float)
                    else Decimal(value)
                )
                values[attr] = value
                validator_func = getattr(
                    sys.modules[__name__],
                    f'validate_{attr}'
                )
                valid.append(validator_func(value))
        valid.append(
            await validate_acceptance_severity_range(
                organization_id,
                values
            )
        )
    except (
        InvalidAcceptanceDays,
        InvalidAcceptanceSeverity,
        InvalidAcceptanceSeverityRange,
        InvalidNumberAcceptations
    ) as exe:
        await sync_to_async(rollbar.report_message)(
            'Invalid values when updating the policies of an organization',
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


async def validate_acceptance_severity_range(
    organization_id,
    values: OrganizationType
) -> bool:
    success: bool = True
    min_value: Decimal = (
        cast(Decimal, values['min_acceptance_severity'])
        if values.get('min_acceptance_severity', None) is not None
        else await get_min_acceptance_severity(organization_id)
    )
    max_value: Decimal = (
        cast(Decimal, values['max_acceptance_severity'])
        if values.get('max_acceptance_severity', None) is not None
        else await get_max_acceptance_severity(organization_id)
    )
    if min_value >= max_value:
        raise InvalidAcceptanceSeverityRange()
    return success


def validate_max_acceptance_days(value: int) -> bool:
    success: bool = True
    if not Decimal('0') <= value <= DEFAULT_MAX_ACCEPTANCE_DAYS:
        raise InvalidAcceptanceDays()
    return success


def validate_max_acceptance_severity(value: Decimal) -> bool:
    success: bool = True
    if not DEFAULT_MIN_SEVERITY <= value <= DEFAULT_MAX_SEVERITY:
        raise InvalidAcceptanceSeverity()
    return success


def validate_max_number_acceptations(value: int) -> bool:
    success: bool = True
    if value < 0:
        raise InvalidNumberAcceptations()
    return success


def validate_min_acceptance_severity(value: Decimal) -> bool:
    success: bool = True
    if not DEFAULT_MIN_SEVERITY <= value <= DEFAULT_MAX_SEVERITY:
        raise InvalidAcceptanceSeverity()
    return success


async def iterate_organizations() -> AsyncIterator[Tuple[str, str]]:
    """Yield pairs of (organization_id, organization_name)."""
    async for org_id, org_name in org_dal.iterate_organizations():
        yield org_id, org_name


async def iterate_organizations_and_groups() -> AsyncIterator[
    Tuple[str, str, Tuple[str, ...]]
]:
    """Yield (org_id, org_name, org_groups) non-concurrently generated."""
    async for org_id, org_name in org_dal.iterate_organizations():
        yield org_id, org_name, await get_groups(org_id)
