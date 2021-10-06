from aioextensions import (
    collect,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations,
    InvalidOrganization,
    OrganizationNotFound,
    UserNotInOrganization,
)
from custom_types import (
    Organization as OrganizationType,
)
from decimal import (
    Decimal,
)
from graphql import (
    GraphQLError,
)
from group_access import (
    domain as group_access_domain,
)
import logging
import logging.config
from names import (
    domain as names_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    dal as orgs_dal,
)
from settings import (
    LOGGING,
)
import sys
from typing import (
    Any,
    AsyncIterator,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from users import (
    domain as users_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")
LOGGER = logging.getLogger(__name__)


async def _add_updated_max_acceptance_days(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
) -> OrganizationType:
    new_max_acceptance_days = values.get("max_acceptance_days")
    organization_data = await loaders.organization.load(organization_id)
    max_acceptance_days: Optional[Decimal] = organization_data[
        "max_acceptance_days"
    ]
    if new_max_acceptance_days != max_acceptance_days:
        return {"max_acceptance_days": new_max_acceptance_days}
    return {}


async def _add_updated_max_acceptance_severity(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
) -> OrganizationType:
    new_max_acceptance_severity = values.get("max_acceptance_severity")
    organization_data = await loaders.organization.load(organization_id)
    max_acceptance_severity: Decimal = organization_data[
        "max_acceptance_severity"
    ]
    if new_max_acceptance_severity != max_acceptance_severity:
        return {"max_acceptance_severity": new_max_acceptance_severity}
    return {}


async def _add_updated_max_number_acceptations(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
    email: str,
    date: str,
) -> OrganizationType:
    new_max_number_acceptation = values.get("max_number_acceptations")
    organization_data = await loaders.organization.load(organization_id)
    max_number_acceptations: Optional[Decimal] = organization_data[
        "max_number_acceptations"
    ]
    if new_max_number_acceptation != max_number_acceptations:
        historic_max_number_acceptation = organization_data[
            "historic_max_number_acceptations"
        ]
        historic_max_number_acceptation.append(
            {
                "date": date,
                "max_number_acceptations": new_max_number_acceptation,
                "user": email,
            }
        )
        return {
            "historic_max_number_acceptations": historic_max_number_acceptation
        }
    return {}


async def _add_updated_min_acceptance_severity(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
) -> OrganizationType:
    new_min_acceptance_severity = values.get("min_acceptance_severity")
    organization_data = await loaders.organization.load(organization_id)
    min_acceptance_severity: Decimal = organization_data[
        "min_acceptance_severity"
    ]
    if new_min_acceptance_severity != min_acceptance_severity:
        return {"min_acceptance_severity": new_min_acceptance_severity}
    return {}


async def _get_new_policies(
    loaders: Any,
    organization_id: str,
    email: str,
    values: Dict[str, Optional[Decimal]],
) -> Union[OrganizationType, None]:
    date = datetime_utils.get_now_as_str()
    policies = await collect(
        [
            _add_updated_max_acceptance_days(loaders, organization_id, values),
            _add_updated_max_number_acceptations(
                loaders, organization_id, values, email, date
            ),
            _add_updated_max_acceptance_severity(
                loaders, organization_id, values
            ),
            _add_updated_min_acceptance_severity(
                loaders, organization_id, values
            ),
        ]
    )
    new_policies: OrganizationType = {
        key: val for item in policies for key, val in item.items()
    }
    return new_policies or None


async def add_group(organization_id: str, group: str) -> bool:
    success = await orgs_dal.add_group(organization_id, group)
    if success:
        users = await get_users(organization_id)
        users_roles = await collect(
            authz.get_organization_level_role(user, organization_id)
            for user in users
        )
        success = success and all(
            await collect(
                group_access_domain.add_user_access(
                    user, group, "system_owner"
                )
                for user, user_role in zip(users, users_roles)
                if user_role in {"system_owner", "group_manager"}
            )
        )
    return success


async def add_user(organization_id: str, email: str, role: str) -> bool:
    # Check for system owner granting requirements
    validate_role_fluid_reqs(email, role)
    success = await orgs_dal.add_user(
        organization_id, email
    ) and await authz.grant_organization_level_role(
        email, organization_id, role
    )
    if success and role in {"system_owner", "group_manager"}:
        groups = await get_groups(organization_id)
        success = success and all(
            await collect(
                group_access_domain.add_user_access(email, group, role)
                for group in groups
            )
        )
    return success


async def add_organization(name: str, email: str) -> OrganizationType:
    new_organization: OrganizationType = {}

    if not await names_domain.exists(name, "organization"):
        raise InvalidOrganization()

    new_organization = await get_or_add(name, email)
    await names_domain.remove(name, "organization")
    return new_organization


async def remove_organization(organization_id: str) -> bool:
    organization_name = await get_name_by_id(organization_id)
    success = await orgs_dal.remove(organization_id, organization_name)
    return success


def format_organization(organization: OrganizationType) -> OrganizationType:
    historic_policies: List[Dict[str, Decimal]] = cast(
        List[Dict[str, Decimal]],
        organization.get("historic_max_number_acceptations", []),
    )
    max_number_acceptations: Optional[Decimal] = (
        historic_policies[-1]["max_number_acceptations"]
        if historic_policies
        else None
    )
    return {
        **organization,
        "historic_max_number_acceptations": organization.get(
            "historic_max_number_acceptations", []
        ),
        "max_acceptance_days": organization.get(
            "max_acceptance_days",
        ),
        "max_acceptance_severity": organization.get(
            "max_acceptance_severity", DEFAULT_MAX_SEVERITY
        ),
        "max_number_acceptations": max_number_acceptations,
        "min_acceptance_severity": organization.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
    }


async def get_by_id(org_id: str) -> OrganizationType:
    organization: OrganizationType = await orgs_dal.get_by_id(org_id)
    if organization:
        return format_organization(organization)
    raise OrganizationNotFound()


async def get_by_name(name: str) -> OrganizationType:
    organization: OrganizationType = await orgs_dal.get_by_name(name.lower())
    if organization:
        return format_organization(organization)
    raise OrganizationNotFound()


async def get_groups(organization_id: str) -> Tuple[str, ...]:
    """Return a tuple of group names for the provided organization."""
    return tuple(await orgs_dal.get_groups(organization_id))


async def get_id_by_name(organization_name: str) -> str:
    result: OrganizationType = await orgs_dal.get_by_name(
        organization_name.lower(), ["id"]
    )
    if not result:
        raise InvalidOrganization()
    return str(result["id"])


async def get_id_for_group(group_name: str) -> str:
    return await orgs_dal.get_id_for_group(group_name)


async def get_name_by_id(organization_id: str) -> str:
    result: OrganizationType = await orgs_dal.get_by_id(
        organization_id, ["name"]
    )
    if not result:
        raise InvalidOrganization()
    return str(result["name"])


async def get_or_add(
    organization_name: str, email: str = ""
) -> OrganizationType:
    """
    Return an organization, even if it does not exists,
    in which case it will be added
    """
    org_created: bool = False
    org_role: str = "customer"
    organization_name = organization_name.lower().strip()

    org = await orgs_dal.get_by_name(organization_name, ["id", "name"])
    if org:
        has_access = (
            await has_user_access(str(org["id"]), email) if email else True
        )
    else:
        org = await orgs_dal.create(organization_name)
        org_created = True
        org_role = "customeradmin"

    if email and (org_created or not has_access):
        await add_user(str(org["id"]), email, org_role)
    return org


async def get_pending_deletion_date_str(organization_id: str) -> Optional[str]:
    result = cast(
        Dict[str, str],
        await orgs_dal.get_by_id(organization_id, ["pending_deletion_date"]),
    )
    return result.get("pending_deletion_date")


async def get_user_organizations(email: str) -> List[str]:
    return await orgs_dal.get_ids_for_user(email)


async def get_users(organization_id: str) -> List[str]:
    return await orgs_dal.get_users(organization_id)


async def has_group(organization_id: str, group_name: str) -> bool:
    return await orgs_dal.has_group(organization_id, group_name)


async def has_user_access(organization_id: str, email: str) -> bool:
    return (
        await orgs_dal.has_user_access(organization_id, email)
        or await authz.get_organization_level_role(email, organization_id)
        == "admin"
    )


async def iterate_organizations() -> AsyncIterator[Tuple[str, str]]:
    """Yield pairs of (organization_id, organization_name)."""
    async for org_id, org_name in orgs_dal.iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield org_id, org_name  # NOSONAR


async def iterate_organizations_and_groups() -> AsyncIterator[
    Tuple[str, str, Tuple[str, ...]]
]:
    """Yield (org_id, org_name, org_groups) non-concurrently generated."""
    async for org_id, org_name in orgs_dal.iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield org_id, org_name, await get_groups(org_id)  # NOSONAR


async def remove_group(group_name: str, organization_id: str) -> bool:
    today = datetime_utils.get_now()
    values: OrganizationType = {
        "deletion_date": datetime_utils.get_as_str(today)
    }
    return await orgs_dal.update_group(organization_id, group_name, values)


async def remove_user(organization_id: str, email: str) -> bool:
    if not await has_user_access(organization_id, email):
        raise UserNotInOrganization()

    user_removed = await orgs_dal.remove_user(organization_id, email)
    role_removed = await authz.revoke_organization_level_role(
        email, organization_id
    )

    org_groups = await get_groups(organization_id)
    groups_removed = all(
        await collect(
            group_access_domain.remove_access(email, group)
            for group in org_groups
        )
    )

    has_orgs = bool(await get_user_organizations(email))
    if not has_orgs:
        user_removed = user_removed and await users_domain.delete(email)
    return user_removed and role_removed and groups_removed


async def update_pending_deletion_date(
    organization_id: str,
    organization_name: str,
    pending_deletion_date: Optional[str],
) -> bool:
    """Update pending deletion date"""
    values: OrganizationType = {"pending_deletion_date": pending_deletion_date}
    success = await orgs_dal.update(organization_id, organization_name, values)
    return success


async def update_policies(
    loaders: Any,
    organization_id: str,
    organization_name: str,
    email: str,
    values: Dict[str, Optional[Decimal]],
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
                    Decimal(value).quantize(Decimal("0.1"))
                    if isinstance(value, float)
                    else Decimal(value)
                )
                values[attr] = value
                validator_func = getattr(
                    sys.modules[__name__], f"validate_{attr}"
                )
                valid.append(validator_func(value))
        valid.append(
            await validate_acceptance_severity_range(
                loaders, organization_id, values
            )
        )
    except (
        InvalidAcceptanceDays,
        InvalidAcceptanceSeverity,
        InvalidAcceptanceSeverityRange,
        InvalidNumberAcceptations,
    ) as exe:
        LOGGER.exception(exe, extra={"extra": locals()})
        raise GraphQLError(str(exe)) from exe

    if all(valid):
        success = True
        new_policies = await _get_new_policies(
            loaders, organization_id, email, values
        )
        if new_policies:
            success = await orgs_dal.update(
                organization_id, organization_name, new_policies
            )
    return success


async def validate_acceptance_severity_range(
    loaders: Any, organization_id: str, values: Dict[str, Optional[Decimal]]
) -> bool:
    success: bool = True
    organization_data = await loaders.organization.load(organization_id)
    min_acceptance_severity: Decimal = organization_data[
        "min_acceptance_severity"
    ]
    max_acceptance_severity: Decimal = organization_data[
        "max_acceptance_severity"
    ]
    min_value: Decimal = (
        cast(Decimal, values["min_acceptance_severity"])
        if values.get("min_acceptance_severity", None) is not None
        else min_acceptance_severity
    )
    max_value: Decimal = (
        cast(Decimal, values["max_acceptance_severity"])
        if values.get("max_acceptance_severity", None) is not None
        else max_acceptance_severity
    )
    if min_value > max_value:
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
