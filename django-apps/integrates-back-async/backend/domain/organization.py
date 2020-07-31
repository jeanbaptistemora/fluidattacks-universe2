import logging
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

from graphql import GraphQLError

from backend import (
    authz,
    util
)
from backend.dal import organization as org_dal
from backend.domain import project as project_domain
from backend.exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations,
    InvalidOrganization,
    UserNotInOrganization
)
from backend.typing import Organization as OrganizationType
from backend.utils import aio


# Constants
DEFAULT_MAX_SEVERITY = Decimal('10.0')
DEFAULT_MIN_SEVERITY = Decimal('0.0')
LOGGER = logging.getLogger(__name__)


async def add_user(organization_id: str, email: str, role: str) -> bool:
    user_added = await org_dal.add_user(organization_id, email)
    role_added = await authz.grant_organization_level_role(
        email,
        organization_id,
        role
    )
    util.invalidate_cache(organization_id.lower())
    return user_added and role_added


async def delete_organization(organization_id: str) -> bool:
    users = await get_users(organization_id)
    users_removed = await aio.materialize(
        remove_user(organization_id, user)
        for user in users
    )
    success = all(users_removed) if users else True

    organization_name = await get_name_by_id(organization_id)
    success = (
        success and
        await org_dal.delete(organization_id, organization_name)
    )

    return success


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


async def get_user_organizations(email: str) -> List[str]:
    return await org_dal.get_ids_for_user(email)


async def get_users(organization_id: str) -> List[str]:
    return await org_dal.get_users(organization_id)


async def has_group(group_name: str, organization_id: str) -> bool:
    return await org_dal.has_group(group_name, organization_id)


async def has_user_access(email: str, organization_id: str) -> bool:
    return await org_dal.has_user_access(email, organization_id) \
        or authz.get_organization_level_role(email, organization_id) == 'admin'


async def remove_user(organization_id: str, email: str) -> bool:
    if not await has_user_access(email, organization_id):
        raise UserNotInOrganization()

    user_removed = await org_dal.remove_user(organization_id, email)
    role_removed = await aio.ensure_io_bound(
        authz.revoke_organization_level_role,
        email,
        organization_id
    )

    org_groups = await get_groups(organization_id)
    groups_removed = all(
        await aio.materialize(
            project_domain.remove_user_access(
                group,
                email,
                check_org_access=False
            )
            for group in org_groups
        )
    )
    return user_removed and role_removed and groups_removed


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
        LOGGER.exception(exe, extra={'extra': locals()})
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
    if value < 0:
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
