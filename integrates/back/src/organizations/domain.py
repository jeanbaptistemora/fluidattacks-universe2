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
    GroupNotFound,
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
from db_model import (
    credentials as credentials_model,
    organizations as orgs_model,
    roots as roots_model,
)
from db_model.credentials.types import (
    Credential,
    CredentialNewState,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationMetadataToUpdate,
    OrganizationPolicies,
    OrganizationPoliciesToUpdate,
    OrganizationState,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from decimal import (
    Decimal,
)
from group_access import (
    domain as group_access_domain,
)
from jose import (
    JWTError,
)
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
    validations as orgs_validations,
)
from organizations.types import (
    CredentialAttributesToAdd,
)
import re
import sys
from typing import (
    Any,
    AsyncIterator,
    Union,
)
from users import (
    domain as users_domain,
)
import uuid

# Constants
DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")


async def add_credential(
    loaders: Any,
    attributes: CredentialAttributesToAdd,
    organization_id: str,
    modified_by: str,
) -> None:
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret] = (
        SshSecret(key=attributes.key or "")
        if attributes.type is CredentialType.SSH
        else HttpsPatSecret(token=attributes.token)
        if attributes.token is not None
        else HttpsSecret(
            user=attributes.user or "",
            password=attributes.password or "",
        )
    )
    credential = Credential(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=modified_by,
        state=CredentialNewState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            name=attributes.name,
            secret=secret,
            type=attributes.type,
        ),
    )
    await orgs_validations.validate_credential_name_in_organization(
        loaders, credential
    )
    await credentials_model.add_new(credential=credential)


async def add_group_access(organization_id: str, group_name: str) -> bool:
    users = await get_users(organization_id)
    users_roles = await collect(
        authz.get_organization_level_role(user, organization_id)
        for user in users
    )
    return all(
        await collect(
            group_access_domain.add_user_access(
                user, group_name, "customer_manager"
            )
            for user, user_role in zip(users, users_roles)
            if user_role == "customer_manager"
        )
    )


async def add_user(
    loaders: Any, organization_id: str, email: str, role: str
) -> bool:
    # Check for customer manager granting requirements
    organization_id = add_org_id_prefix(organization_id)
    validate_role_fluid_reqs(email, role)
    success = await orgs_dal.add_user(
        organization_id, email
    ) and await authz.grant_organization_level_role(
        email, organization_id, role
    )
    if success and role == "customer_manager":
        org_groups = await get_group_names(loaders, organization_id)
        success = success and all(
            await collect(
                group_access_domain.add_user_access(email, group, role)
                for group in org_groups
            )
        )
    return success


async def update_state(
    organization_id: str,
    organization_name: str,
    state: OrganizationState,
) -> None:
    await orgs_model.update_state(
        organization_id=organization_id,
        organization_name=organization_name,
        state=state,
    )


async def get_access_by_url_token(
    url_token: str,
) -> dict[str, Any]:
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
    active_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_active_groups = list(groups_utils.filter_active_groups(org_groups))
        active_groups.extend(org_active_groups)
    return tuple(active_groups)


async def get_all_active_group_names(
    loaders: Any,
) -> tuple[str, ...]:
    active_groups = await get_all_active_groups(loaders)
    active_group_names = tuple(group.name for group in active_groups)
    return active_group_names


async def get_all_deleted_groups(
    loaders: Any,
) -> tuple[Group, ...]:
    deleted_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_active_groups = list(
            groups_utils.filter_deleted_groups(org_groups)
        )
        deleted_groups.extend(org_active_groups)
    return tuple(deleted_groups)


async def get_group_names(
    loaders: Any, organization_id: str
) -> tuple[str, ...]:
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization_id
    )
    return tuple(group.name for group in org_groups)


async def exists(loaders: Any, organization_name: str) -> bool:
    try:
        await loaders.organization.load(organization_name.lower().strip())
        return True
    except OrganizationNotFound:
        return False


async def add_organization(
    loaders: Any, organization_name: str, email: str
) -> Organization:
    if await exists(loaders, organization_name):
        raise InvalidOrganization("Name taken")
    if not re.match(r"^[a-zA-Z]{4,10}$", organization_name):
        raise InvalidOrganization("Invalid name")

    modified_date = datetime_utils.get_iso_date()
    organization = Organization(
        id=add_org_id_prefix(str(uuid.uuid4())),
        name=organization_name.lower().strip(),
        policies=OrganizationPolicies(
            modified_by=email,
            modified_date=modified_date,
        ),
        state=OrganizationState(
            modified_by=email,
            modified_date=modified_date,
            status=OrganizationStateStatus.ACTIVE,
        ),
    )
    await orgs_model.add(organization=organization)
    if email:
        await add_user(loaders, organization.id, email, "user_manager")
    return organization


async def get_or_add(
    loaders: Any, organization_name: str, email: str = ""
) -> Organization:
    if await exists(loaders, organization_name):
        org: Organization = await loaders.organization.load(organization_name)
        org_id = remove_org_id_prefix(org.id)
        has_access = await has_user_access(org_id, email) if email else True

        if email and not has_access:
            await add_user(loaders, org_id, email, "user_manager")
    else:
        org = await add_organization(loaders, organization_name, email)
    return org


async def get_user_access(organization_id: str, email: str) -> dict[str, Any]:
    return await orgs_dal.get_access_by_url_token(organization_id, email)


async def get_user_organizations(email: str) -> list[str]:
    return await orgs_dal.get_ids_for_user(email)


async def get_users(organization_id: str) -> list[str]:
    return await orgs_dal.get_users(organization_id)


async def has_group(
    loaders: Any, organization_id: str, group_name: str
) -> bool:
    try:
        group: Group = await loaders.group.load(group_name)
        return group.organization_id == organization_id
    except GroupNotFound:
        return False


async def has_user_access(organization_id: str, email: str) -> bool:
    organization_id = add_org_id_prefix(organization_id)
    return (
        await orgs_dal.has_user_access(organization_id, email)
        or await authz.get_organization_level_role(email, organization_id)
        == "admin"
    )


async def invite_to_organization(
    loaders: Any,
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
        organization: Organization = await loaders.organization.load(
            organization_name
        )
        organization_id = organization.id
        url_token = token.new_encoded_jwt(
            {
                "organization_id": organization_id,
                "user_email": email,
            },
        )
        success = await update_user(
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
        user_role = await authz.get_user_level_role(modified_by)
        email_context: dict[str, Any] = {
            "admin": email,
            "group": organization_name,
            "responsible": modified_by,
            "confirm_access_url": confirm_access_url,
            "reject_access_url": reject_access_url,
            "user_role": user_role.replace("_", " "),
        }
        schedule(groups_mail.send_mail_access_granted(mail_to, email_context))
    return success


async def iterate_organizations() -> AsyncIterator[Organization]:
    async for organization in orgs_model.iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield organization  # NOSONAR


async def iterate_organizations_and_groups(
    loaders: Any,
) -> AsyncIterator[tuple[str, str, tuple[str, ...]]]:
    """Yield (org_id, org_name, org_group_names) non-concurrently generated."""
    async for organization in iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield organization.id, organization.name, await get_group_names(
            loaders, organization.id
        )  # NOSONAR


async def remove_credential(
    loaders: Any, organization_id: str, credential_id: str, modified_by: str
) -> None:
    organization: Organization = await loaders.organization.load(credential_id)
    organization_roots: tuple[
        Root, ...
    ] = await loaders.organization_roots.load(organization.name)
    await collect(
        roots_model.update_root_state(
            current_value=root.state,
            group_name=root.group_name,
            root_id=root.id,
            state=root.state._replace(
                credential_id=None,
                modified_by=modified_by,
                modified_date=datetime_utils.get_iso_date(),
            ),
        )
        for root in organization_roots
        if isinstance(root, GitRoot)
        and root.state.credential_id == credential_id
    )
    await credentials_model.remove_new(
        credential_id=credential_id,
        organization_id=organization_id,
    )


async def remove_user(
    loaders: Any, organization_id: str, email: str, modified_by: str
) -> bool:
    organization_id = add_org_id_prefix(organization_id)
    if not await has_user_access(organization_id, email):
        raise UserNotInOrganization()

    user_removed, role_removed = await collect(
        (
            orgs_dal.remove_user(organization_id, email),
            authz.revoke_organization_level_role(email, organization_id),
        )
    )

    org_group_names = await get_group_names(loaders, organization_id)
    groups_removed = all(
        await collect(
            tuple(
                group_access_domain.remove_access(loaders, email, group)
                for group in org_group_names
            )
        )
    )

    has_orgs = bool(await get_user_organizations(email))
    if not has_orgs:
        user_removed = user_removed and await users_domain.delete(email)
    user_credentials: tuple[
        Credential, ...
    ] = await loaders.user_credentials_new.load(email)
    await collect(
        tuple(
            remove_credential(
                loaders=loaders,
                organization_id=organization_id,
                credential_id=credential.id,
                modified_by=modified_by,
            )
            for credential in user_credentials
        )
    )
    return user_removed and role_removed and groups_removed


async def reject_register_for_organization_invitation(
    loaders: Any,
    organization_access: dict[str, Any],
) -> bool:
    success: bool = False
    invitation = organization_access["invitation"]
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access["pk"]
    user_email = organization_access["sk"].split("#")[1]
    success = await remove_user(
        loaders, organization_id, user_email, user_email
    )
    return success


async def update_user(
    organization_id: str,
    user_email: str,
    data: dict[str, Any],
) -> bool:
    return await orgs_dal.update_user(organization_id, user_email, data)


async def update_invited_stakeholder(
    email: str,
    invitation: dict[str, Any],
    organization_id: str,
    role: str,
) -> bool:
    success = False
    new_invitation = invitation.copy()
    if validate_role_fluid_reqs(email, role):
        new_invitation["role"] = role
        success = await update_user(
            organization_id,
            email,
            {
                "invitation": new_invitation,
            },
        )
    return success


async def update_billing_customer(
    organization_id: str,
    organization_name: str,
    billing_customer: str,
) -> None:
    """Update Stripe billing customer."""
    await orgs_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            billing_customer=billing_customer
        ),
        organization_id=organization_id,
        organization_name=organization_name,
    )


async def update_policies(
    loaders: Any,
    organization_id: str,
    organization_name: str,
    user_email: str,
    policies_to_update: OrganizationPoliciesToUpdate,
) -> None:
    validated_policies: dict[str, Any] = {}
    for attr, value in policies_to_update._asdict().items():
        if value is not None:
            value = (
                Decimal(value).quantize(Decimal("0.1"))
                if isinstance(value, float)
                else Decimal(value)
            )
            validated_policies[attr] = value
            validator_func = getattr(sys.modules[__name__], f"validate_{attr}")
            validator_func(value)
    await validate_acceptance_severity_range(
        loaders, organization_id, policies_to_update
    )

    if validated_policies:
        today = datetime_utils.get_iso_date()
        await orgs_model.update_policies(
            modified_by=user_email,
            modified_date=today,
            organization_id=organization_id,
            organization_name=organization_name,
            policies=policies_to_update,
        )
        await send_mail_policies(
            loaders=loaders,
            new_policies=policies_to_update._asdict(),
            organization_id=organization_id,
            organization_name=organization_name,
            responsible=user_email,
            date=today,
        )


# pylint: disable=too-many-arguments
async def send_mail_policies(
    loaders: Any,
    new_policies: dict[str, Any],
    organization_id: str,
    organization_name: str,
    responsible: str,
    date: str,
) -> None:
    organization_data: Organization = await loaders.organization.load(
        organization_id
    )
    policies_format = {
        "max_acceptance_days": (
            "Maximum number of calendar days a finding "
            "can be temporarily accepted"
        ),
        "max_acceptance_severity": (
            "Maximum temporal CVSS 3.1 score range "
            "between which a finding can be accepted"
        ),
        "min_breaking_severity": (
            "Minimum CVSS 3.1 score of an open "
            "vulnerability for DevSecOps to break the build in strict mode"
        ),
        "min_acceptance_severity": (
            "Minimum temporal CVSS 3.1 score range "
            "between which a finding can be accepted"
        ),
        "vulnerability_grace_period": (
            "Grace period in days where newly "
            "reported vulnerabilities won't break the build (DevSecOps only)"
        ),
        "max_number_acceptances": (
            "Maximum number of times a finding can be temporarily accepted"
        ),
    }

    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = organization_data.policies._asdict().get(key)
        if val is not None and val != old_value:
            policies_content[policies_format[key]] = {
                "from": old_value,
                "to": val,
            }

    email_context: dict[str, Any] = {
        "org_name": organization_name,
        "policies_link": f"{BASE_URL}/orgs/{organization_name}/policies",
        "policies_content": policies_content,
        "responsible": responsible,
        "date": datetime_utils.get_datetime_from_iso_str(date),
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


async def validate_acceptance_severity_range(
    loaders: Any, organization_id: str, values: OrganizationPoliciesToUpdate
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
