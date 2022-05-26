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
from db_model.groups.types import (
    Group,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationPolicies,
    OrganizationState,
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
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
    token,
)
from newutils.organizations import (
    add_org_id_prefix,
    remove_org_id_prefix,
)
from newutils.validations import (
    validate_email_address,
)
from organizations import (
    dal as orgs_dal,
)
import re
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
)
from users import (
    domain as users_domain,
)
import uuid

logging.config.dictConfig(LOGGING)

# Constants
DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")
LOGGER = logging.getLogger(__name__)


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
    organization_id = add_org_id_prefix(organization_id)
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


async def add_organization(name: str, email: str) -> Dict[str, Any]:
    if not re.match(r"^[a-zA-Z]{4,10}$", name):
        raise InvalidOrganization()

    org = await orgs_dal.get_by_name(name, ["id"])
    if org:
        raise InvalidOrganization()

    new_organization = await get_or_add(name, email)
    return new_organization


async def remove_organization(organization_id: str, modified_by: str) -> bool:
    return await orgs_dal.remove(
        organization_id=organization_id,
        modified_by=modified_by,
    )


def format_organization(organization: Dict[str, Any]) -> Dict[str, Any]:
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


async def get_all_active_groups(
    loaders: Any,
) -> tuple[Group, ...]:
    all_groups_names: list[str] = []
    async for _, _, org_group_names in iterate_organizations_and_groups():
        all_groups_names.extend(org_group_names)
    all_groups = await loaders.group.load_many(all_groups_names)
    return groups_utils.filter_active_groups(tuple(all_groups))


async def get_all_active_group_names(
    loaders: Any,
) -> tuple[str, ...]:
    active_groups = await get_all_active_groups(loaders)
    active_group_names = tuple(group.name for group in active_groups)
    return active_group_names


async def get_by_name(name: str) -> Dict[str, Any]:
    organization: Dict[str, Any] = await orgs_dal.get_by_name(name.lower())
    if organization:
        return format_organization(organization)
    raise OrganizationNotFound()


async def get_groups(organization_id: str) -> Tuple[str, ...]:
    """Return a tuple of group names for the provided organization."""
    return tuple(await orgs_dal.get_groups(organization_id))


async def get_id_by_name(organization_name: str) -> str:
    result: Dict[str, Any] = await orgs_dal.get_by_name(
        organization_name.lower(), ["id"]
    )
    if not result:
        raise OrganizationNotFound()
    return str(result["id"])


async def get_id_for_group(group_name: str) -> str:
    return await orgs_dal.get_id_for_group(group_name)


async def get_name_by_id(organization_id: str) -> str:
    result: Dict[str, Any] = await orgs_dal.get_by_id(
        organization_id, ["name"]
    )
    if not result:
        raise OrganizationNotFound()
    return str(result["name"])


async def if_exist(organization_name: str) -> bool:
    if await orgs_dal.get_by_name(organization_name.lower().strip()):
        return True
    return False


async def add_organization_typed(
    organization_name: str, email: str
) -> Organization:
    if await if_exist(organization_name) or not re.match(
        r"^[a-zA-Z]{4,10}$", organization_name
    ):
        raise InvalidOrganization()
    org = Organization(
        id=str(uuid.uuid4()),
        name=organization_name.lower().strip(),
        policies=OrganizationPolicies(),
        state=OrganizationState(
            modified_by=email,
            modified_date=datetime_utils.get_iso_date(),
            status=OrganizationStateStatus.ACTIVE,
        ),
    )
    await orgs_dal.add_typed(org)
    org_role = "user_manager"
    if email and org:
        await add_user(f"ORG#{org.id}", email, org_role)
    return org


async def get_or_add(
    organization_name: str, email: str = ""
) -> Dict[str, Any]:
    """
    Return an organization, even if it does not exists,
    in which case it will be added
    """
    org_created: bool = False
    org_role: str = "user"
    organization_name = organization_name.lower().strip()

    org = await orgs_dal.get_by_name(organization_name, ["id", "name"])
    if org:
        org["id"] = remove_org_id_prefix(org["id"])
        has_access = (
            await has_user_access(str(org["id"]), email) if email else True
        )
    else:
        org = await orgs_dal.add(
            modified_by=email,
            organization_name=organization_name,
        )
        org_created = True
        org_role = "user_manager"

    if email and (org_created or not has_access):
        await add_user(str(org["id"]), email, org_role)
    return org


async def get_user_access(organization_id: str, email: str) -> Dict[str, Any]:
    return await orgs_dal.get_access_by_url_token(organization_id, email)


async def get_user_organizations(email: str) -> List[str]:
    return await orgs_dal.get_ids_for_user(email)


async def get_users(organization_id: str) -> List[str]:
    return await orgs_dal.get_users(organization_id)


async def has_group(organization_id: str, group_name: str) -> bool:
    return await orgs_dal.has_group(organization_id, group_name)


async def has_user_access(organization_id: str, email: str) -> bool:
    organization_id = add_org_id_prefix(organization_id)
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
        email_context: dict[str, Any] = {
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
    values: Dict[str, Any] = {
        "deletion_date": datetime_utils.get_as_str(today)
    }
    return await orgs_dal.update_group(organization_id, group_name, values)


async def remove_user(loaders: Any, organization_id: str, email: str) -> bool:
    organization_id = add_org_id_prefix(organization_id)
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
    values: Dict[str, Any] = {"pending_deletion_date": pending_deletion_date}
    success = await orgs_dal.update(organization_id, organization_name, values)
    return success


async def update_billing_customer(
    org_id: str,
    org_name: str,
    org_billing_customer: str,
) -> bool:
    """Update Stripe billing customer"""
    values: Dict[str, Any] = {"billing_customer": org_billing_customer}
    success = await orgs_dal.update(org_id, org_name, values)
    return success


async def update_policies(
    loaders: Any,
    organization_id: str,
    organization_name: str,
    email: str,
    org_policies: OrganizationPolicies,
) -> bool:
    success: bool = False
    valid: List[bool] = []
    try:
        for attr, value in org_policies._asdict().items():
            if value is not None:
                value = (
                    Decimal(value).quantize(Decimal("0.1"))
                    if isinstance(value, float)
                    else Decimal(value)
                )
                org_policies._asdict()[attr] = value
                validator_func = getattr(
                    sys.modules[__name__], f"validate_{attr}"
                )
                valid.append(validator_func(value))
        valid.append(
            await validate_acceptance_severity_range_typed(
                loaders, organization_id, org_policies
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
        organization: Organization = await loaders.organization.load(
            organization_id
        )
        org_policies_to_update = organization.policies
        new_policies = org_policies_to_update._replace(
            max_acceptance_days=org_policies.max_acceptance_days,
            max_acceptance_severity=org_policies.max_acceptance_severity,
            max_number_acceptances=org_policies.max_number_acceptances,
            min_acceptance_severity=org_policies.min_acceptance_severity,
            min_breaking_severity=org_policies.min_breaking_severity,
            vulnerability_grace_period=org_policies.vulnerability_grace_period,
            modified_date=datetime_utils.get_iso_date(),
            modified_by=email,
        )
        if new_policies:
            success = await orgs_dal.update_policies_typed(
                organization_id=organization_id,
                organization_name=organization_name,
                policies=new_policies,
            )
            policies_to_mail = new_policies._replace(
                modified_date=None,
                modified_by=None,
            )
            await send_mail_policies(
                loaders,
                policies_to_mail._asdict(),
                organization_id,
                organization_name,
                email,
                date=new_policies.modified_date,
            )

    return success


# pylint: disable=too-many-arguments
async def send_mail_policies(
    loaders: Any,
    new_policies: Dict[str, Any],
    organization_id: str,
    organization_name: str,
    responsible: str,
    date: Optional[str],
) -> None:
    organization_data: Organization = await loaders.organization.load(
        organization_id
    )
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
        "max_number_acceptances": "Maximum number of times a "
        "finding can be temporarily accepted",
    }

    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = organization_data.policies._asdict().get(key)
        if val is not None and val != old_value:
            policies_content[policies_format[key]] = {
                "from": old_value,
                "to": val,
            }

    email_context: Dict[str, Any] = {
        "org_name": organization_name,
        "policies_link": (f"{BASE_URL}/orgs/{organization_name}/policies"),
        "policies_content": policies_content,
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

    if policies_content:
        await groups_mail.send_mail_updated_policies(
            email_to=stakeholders_emails,
            context=email_context,
        )


async def validate_acceptance_severity_range_typed(
    loaders: Any, organization_id: str, values: OrganizationPolicies
) -> bool:
    success: bool = True
    organization_data: Organization = await loaders.organization.load(
        organization_id
    )
    min_acceptance_severity = (
        organization_data.policies.min_acceptance_severity
    )
    max_acceptance_severity = (
        organization_data.policies.max_acceptance_severity
    )
    min_value = (
        values.min_acceptance_severity
        if values.min_acceptance_severity is not None
        else min_acceptance_severity
    )
    max_value = (
        values.max_acceptance_severity
        if values.max_acceptance_severity is not None
        else max_acceptance_severity
    )
    if (
        min_value is not None
        and max_value is not None
        and (min_value > max_value)
    ):
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
