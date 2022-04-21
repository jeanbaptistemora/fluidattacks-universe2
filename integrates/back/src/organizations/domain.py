from aioextensions import (
    collect,
    schedule,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
import bugsnag
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidAuthorization,
    InvalidNumberAcceptances,
    InvalidOrganization,
    InvalidSeverity,
    InvalidVulnerabilityGracePeriod,
    OrganizationNotFound,
    UserNotInOrganization,
)
from custom_types import (
    MailContent as MailContentType,
    Organization as OrganizationType,
)
from db_model.groups.types import (
    Group,
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
from jose import (
    JWTError,
)
import logging
import logging.config
from mailer import (
    groups as groups_mail,
)
from names import (
    domain as names_domain,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
    token,
)
from newutils.utils import (
    get_key_or_fallback,
)
from newutils.validations import (
    validate_email_address,
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


async def _add_updated_values(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
    value_to_update: str,
) -> OrganizationType:
    """Generic method to update org policies and reuse typical validation
    logic"""
    new_value = values.get(value_to_update)
    organization_data = await loaders.organization.load(organization_id)
    old_value: Optional[Decimal] = organization_data.get(value_to_update)
    if new_value is not None and new_value != old_value:
        return {value_to_update: new_value}
    return {}


async def _add_updated_max_number_acceptances(
    loaders: Any,
    organization_id: str,
    values: Dict[str, Optional[Decimal]],
    email: str,
    date: str,
) -> OrganizationType:
    new_max_number_acceptances = get_key_or_fallback(
        values, "max_number_acceptances", "max_number_acceptations"
    )
    organization_data = await loaders.organization.load(organization_id)
    max_number_acceptances: Optional[Decimal] = organization_data[
        "max_number_acceptations"
    ]
    if (
        new_max_number_acceptances is not None
        and new_max_number_acceptances != max_number_acceptances
    ):
        historic_max_number_acceptances = get_key_or_fallback(
            organization_data,
            "historic_max_number_acceptances",
            "historic_max_number_acceptations",
        )
        historic_max_number_acceptances.append(
            {
                "date": date,
                "max_number_acceptations": new_max_number_acceptances,
                "user": email,
            }
        )
        return {
            "historic_max_number_acceptations": historic_max_number_acceptances
        }
    return {}


async def _get_new_policies(
    loaders: Any,
    organization_id: str,
    email: str,
    date: str,
    values: Dict[str, Optional[Decimal]],
) -> Union[OrganizationType, None]:
    policies = await collect(
        [
            _add_updated_max_number_acceptances(
                loaders, organization_id, values, email, date
            ),
            _add_updated_values(
                loaders, organization_id, values, "max_acceptance_days"
            ),
            _add_updated_values(
                loaders, organization_id, values, "max_acceptance_severity"
            ),
            _add_updated_values(
                loaders, organization_id, values, "min_acceptance_severity"
            ),
            _add_updated_values(
                loaders, organization_id, values, "min_breaking_severity"
            ),
            _add_updated_values(
                loaders, organization_id, values, "vulnerability_grace_period"
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
                    user, group, "customer_manager"
                )
                for user, user_role in zip(users, users_roles)
                if user_role == "customer_manager"
            )
        )
    return success


async def add_user(organization_id: str, email: str, role: str) -> bool:
    # Check for customer manager granting requirements
    validate_role_fluid_reqs(email, role)
    success = await orgs_dal.add_user(
        organization_id, email
    ) and await authz.grant_organization_level_role(
        email, organization_id, role
    )
    if success and role == "customer_manager":
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
    max_number_acceptances: Optional[Decimal] = (
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
        "max_number_acceptations": max_number_acceptances,
        "min_acceptance_severity": organization.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
        "min_breaking_severity": organization.get(
            "min_breaking_severity", DEFAULT_MIN_SEVERITY
        ),
    }


async def get_access_by_url_token(
    url_token: str,
) -> Dict[str, Any]:
    access = {}
    try:
        token_content = token.decode_jwt(url_token)
        organization_id: str = token_content["organization_id"]
        user_email: str = token_content["user_email"]
        access = await orgs_dal.get_access_by_url_token(
            organization_id, user_email
        )
    except JWTError:
        InvalidAuthorization()
    return access


async def get_all_active_groups_typed(
    loaders: Any,
) -> tuple[Group, ...]:
    all_groups_names: list[str] = []
    async for _, _, org_group_names in iterate_organizations_and_groups():
        all_groups_names.extend(org_group_names)
    all_groups = await loaders.group_typed.load_many(all_groups_names)
    return groups_utils.filter_active_groups(tuple(all_groups))


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


async def get_name_for_group(group_name: str) -> str:
    organization_id: str = await get_id_for_group(group_name)
    return await get_name_by_id(organization_id)


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
    org_role: str = "user"
    organization_name = organization_name.lower().strip()

    org = await orgs_dal.get_by_name(organization_name, ["id", "name"])
    if org:
        has_access = (
            await has_user_access(str(org["id"]), email) if email else True
        )
    else:
        org = await orgs_dal.create(organization_name)
        org_created = True
        org_role = "user_manager"

    if email and (org_created or not has_access):
        await add_user(str(org["id"]), email, org_role)
    return org


async def get_pending_deletion_date_str(organization_id: str) -> Optional[str]:
    result = cast(
        Dict[str, str],
        await orgs_dal.get_by_id(organization_id, ["pending_deletion_date"]),
    )
    return result.get("pending_deletion_date")


async def get_user_access(organization_id: str, email: str) -> Dict[str, Any]:
    return await orgs_dal.get_access_by_url_token(organization_id, email)


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


async def invite_to_organization(
    email: str,
    role: str,
    organization_name: str,
    modified_by: str,
) -> bool:
    success = False
    if validate_email_address(email) and validate_role_fluid_reqs(email, role):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        organization_id = await get_id_by_name(organization_name)
        url_token = token.new_encoded_jwt(
            {
                "organization_id": organization_id,
                "user_email": email,
            },
        )
        success = await update(
            organization_id,
            email,
            {
                "expiration_time": expiration_time,
                "has_access": False,
                "invitation": {
                    "is_used": False,
                    "role": role,
                    "url_token": url_token,
                },
            },
        )
        confirm_access_url = (
            f"{BASE_URL}/confirm_access_organization/{url_token}"
        )
        reject_access_url = (
            f"{BASE_URL}/reject_access_organization/{url_token}"
        )
        mail_to = [email]
        email_context: MailContentType = {
            "admin": email,
            "group": organization_name,
            "responsible": modified_by,
            "confirm_access_url": confirm_access_url,
            "reject_access_url": reject_access_url,
        }
        schedule(groups_mail.send_mail_access_granted(mail_to, email_context))
    return success


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


async def remove_user(loaders: Any, organization_id: str, email: str) -> bool:
    if not await has_user_access(organization_id, email):
        raise UserNotInOrganization()

    user_removed, role_removed = await collect(
        (
            orgs_dal.remove_user(organization_id, email),
            authz.revoke_organization_level_role(email, organization_id),
        )
    )

    org_groups = await get_groups(organization_id)
    groups_removed = all(
        await collect(
            tuple(
                group_access_domain.remove_access(loaders, email, group)
                for group in org_groups
            )
        )
    )

    has_orgs = bool(await get_user_organizations(email))
    if not has_orgs:
        user_removed = user_removed and await users_domain.delete(email)
    return user_removed and role_removed and groups_removed


async def reject_register_for_organization_invitation(
    loaders: Any,
    organization_access: Dict[str, Any],
) -> bool:
    success: bool = False
    invitation = organization_access["invitation"]
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access["pk"]
    user_email = organization_access["sk"].split("#")[1]
    success = await remove_user(loaders, organization_id, user_email)
    return success


async def update(
    organization_id: str,
    user_email: str,
    data: Dict[str, Any],
) -> bool:
    return await orgs_dal.update_user(organization_id, user_email, data)


async def update_invited_stakeholder(
    email: str,
    invitation: Dict[str, Any],
    organization_id: str,
    role: str,
) -> bool:
    success = False
    new_invitation = invitation.copy()
    if validate_role_fluid_reqs(email, role):
        new_invitation["role"] = role
        success = await update(
            organization_id,
            email,
            {
                "invitation": new_invitation,
            },
        )
    return success


async def update_pending_deletion_date(
    organization_id: str,
    organization_name: str,
    pending_deletion_date: Optional[str],
) -> bool:
    """Update pending deletion date"""
    values: OrganizationType = {"pending_deletion_date": pending_deletion_date}
    success = await orgs_dal.update(organization_id, organization_name, values)
    return success


async def update_billing_customer(
    org_id: str,
    org_name: str,
    org_billing_customer: str,
) -> bool:
    """Update Stripe billing customer"""
    values: OrganizationType = {"billing_customer": org_billing_customer}
    success = await orgs_dal.update(org_id, org_name, values)
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
        InvalidNumberAcceptances,
        InvalidSeverity,
    ) as exe:
        LOGGER.exception(exe, extra={"extra": locals()})
        raise GraphQLError(str(exe)) from exe

    if all(valid):
        success = True
        date = datetime_utils.get_now_as_str()
        # Compatibility for the old API
        if "max_number_acceptances" in values:
            values["max_number_acceptations"] = values.pop(
                "max_number_acceptances"
            )
        new_policies = await _get_new_policies(
            loaders, organization_id, email, date, values
        )
        if new_policies:
            await send_mail_policies(
                loaders,
                new_policies,
                organization_id,
                organization_name,
                email,
                date,
            )
            success = await orgs_dal.update(
                organization_id, organization_name, new_policies
            )
    return success


# pylint: disable=too-many-arguments, too-many-locals
async def send_mail_policies(
    loaders: Any,
    new_policies: Dict[str, Any],
    organization_id: str,
    organization_name: str,
    responsible: str,
    date: str,
) -> None:
    organization_data = await loaders.organization.load(organization_id)
    policies_format = {
        "max_acceptance_days": "Maximum number of calendar days a finding "
        "can be temporarily accepted",
        "max_acceptance_severity": "Maximum temporal CVSS 3.1 score range "
        "between which a finding can be accepted",
        "min_breaking_severity": "Minimum CVSS 3.1 score of an open "
        "vulnerability for DevSecOps to break the build in strict mode",
        "min_acceptance_severity": "Minimum temporal CVSS 3.1 score range "
        "between which a finding can be accepted",
        "vulnerability_grace_period": "Grace period in days where newly "
        "reported vulnerabilities won't break the build (DevSecOps only)",
    }

    policies_content: str = ""
    for key, val in new_policies.items():
        if "historic_max_number_acceptations" in key:
            number_acceptations = val[-1]["max_number_acceptations"]
            old_number_acceptations = organization_data[
                "max_number_acceptations"
            ]
            policies_content += (
                "Maximum number of times a finding can be "
                f"temporarily accepted: from {old_number_acceptations} to "
                f"{number_acceptations}\n"
            )
        else:
            old_value: Optional[Decimal] = organization_data.get(key)
            if val is not None and val != old_value:
                policies_content += (
                    f"{policies_format[key]}: from {old_value} to {val}\n"
                )

    email_context: Dict[str, Any] = {
        "org_name": organization_name,
        "policies_link": (f"{BASE_URL}/orgs/{organization_name}/policies"),
        "policies": policies_content.splitlines(),
        "responsible": responsible,
        "date": date,
    }

    org_stakeholders_loaders = await loaders.organization_stakeholders.load(
        organization_id
    )

    stakeholders_emails = [
        stakeholder["email"]
        for stakeholder in org_stakeholders_loaders
        if stakeholder["role"] in ["customer_manager", "user_manager"]
    ]

    await groups_mail.send_mail_updated_policies(
        email_to=stakeholders_emails,
        context=email_context,
    )


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


def validate_max_number_acceptances(value: int) -> bool:
    success: bool = True
    if value < 0:
        raise InvalidNumberAcceptances()
    return success


def validate_min_acceptance_severity(value: Decimal) -> bool:
    success: bool = True
    if not DEFAULT_MIN_SEVERITY <= value <= DEFAULT_MAX_SEVERITY:
        raise InvalidAcceptanceSeverity()
    return success


def validate_min_breaking_severity(value: Decimal) -> bool:
    success: bool = True
    try:
        float(value)
    except ValueError as error:
        raise InvalidSeverity(
            [DEFAULT_MIN_SEVERITY, DEFAULT_MAX_SEVERITY]
        ) from error
    if not DEFAULT_MIN_SEVERITY <= value <= DEFAULT_MAX_SEVERITY:
        raise InvalidSeverity([DEFAULT_MIN_SEVERITY, DEFAULT_MAX_SEVERITY])
    return success


def validate_vulnerability_grace_period(value: int) -> bool:
    success: bool = True
    if value < 0:
        raise InvalidVulnerabilityGracePeriod()
    return success
