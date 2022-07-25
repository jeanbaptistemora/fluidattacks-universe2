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
    InvalidParameter,
    InvalidSeverity,
    InvalidVulnerabilityGracePeriod,
    OrganizationNotFound,
    StakeholderNotInOrganization,
)
from db_model import (
    credentials as credentials_model,
    organizations as orgs_model,
    roots as roots_model,
)
from db_model.constants import (
    POLICIES_FORMATTED,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    CredentialsState,
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
from db_model.organization_access.enums import (
    InvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
    OrganizationInvitation,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationMetadataToUpdate,
    OrganizationState,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.types import (
    Policies,
    PoliciesToUpdate,
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
    token as token_utils,
)
from newutils.organization_access import (
    format_invitation_state,
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
    utils as orgs_utils,
    validations as orgs_validations,
)
from organizations.types import (
    CredentialAttributesToAdd,
    CredentialAttributesToUpdate,
)
import re
from stakeholders import (
    domain as stakeholders_domain,
)
import sys
from typing import (
    Any,
    AsyncIterator,
    Union,
)
import uuid

# Constants
DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")


async def add_credentials(
    loaders: Any,
    attributes: CredentialAttributesToAdd,
    organization_id: str,
    modified_by: str,
) -> None:
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret] = (
        SshSecret(
            key=orgs_utils.format_credentials_ssh_key(attributes.key or "")
        )
        if attributes.type is CredentialType.SSH
        else HttpsPatSecret(token=attributes.token)
        if attributes.token is not None
        else HttpsSecret(
            user=attributes.user or "",
            password=attributes.password or "",
        )
    )
    credential = Credentials(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=modified_by,
        state=CredentialsState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            name=attributes.name,
            secret=secret,
            type=attributes.type,
        ),
    )
    await orgs_validations.validate_credentials_name_in_organization(
        loaders, credential.organization_id, credential.state.name
    )
    await credentials_model.add(credential=credential)


async def add_group_access(
    loaders: Any, organization_id: str, group_name: str
) -> bool:
    users = await get_stakeholders_emails(loaders, organization_id)
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


async def add_stakeholder(
    loaders: Any, organization_id: str, email: str, role: str
) -> bool:
    # Check for customer manager granting requirements
    organization_id = add_org_id_prefix(organization_id)
    validate_role_fluid_reqs(email, role)
    await orgs_dal.add(
        organization_access=OrganizationAccess(
            organization_id=organization_id, email=email
        )
    )
    success = await authz.grant_organization_level_role(
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
    loaders: Any,
    url_token: str,
) -> OrganizationAccess:
    try:
        token_content = token_utils.decode_jwt(url_token)
        organization_id: str = token_content["organization_id"]
        user_email: str = token_content["user_email"]
    except JWTError:
        InvalidAuthorization()
    access: OrganizationAccess = await loaders.organization_access.load(
        (organization_id, user_email)
    )
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
        policies=Policies(
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
        await add_stakeholder(loaders, organization.id, email, "user_manager")
    return organization


async def get_or_add(
    loaders: Any, organization_name: str, email: str = ""
) -> Organization:
    if not await exists(loaders, organization_name):
        return await add_organization(loaders, organization_name, email)

    organization: Organization = await loaders.organization.load(
        organization_name
    )
    organization_id = remove_org_id_prefix(organization.id)
    if email and not await has_access(loaders, organization_id, email):
        await add_stakeholder(loaders, organization_id, email, "user_manager")

    return organization


async def get_stakeholder_role(
    loaders: Any,
    email: str,
    is_registered: bool,
    organization_id: str,
) -> str:
    user_access: OrganizationAccess = await loaders.organization_access.load(
        (organization_id, email)
    )
    if user_access.invitation:
        invitation: OrganizationInvitation = user_access.invitation
        invitation_state = format_invitation_state(invitation, is_registered)
        if invitation_state == InvitiationState.PENDING:
            stakeholder_role = invitation.role
    else:
        stakeholder_role = await authz.get_organization_level_role(
            email, organization_id
        )

    return stakeholder_role


async def get_stakeholders(
    loaders: Any, organization_id: str
) -> tuple[Stakeholder, ...]:
    stakeholders_access: tuple[
        OrganizationAccess, ...
    ] = await loaders.organization_stakeholders_access.load(organization_id)
    stakeholder_emails = [access.email for access in stakeholders_access]
    stakeholders = [
        await loaders.stakeholder.load(email)
        if await stakeholders_domain.exists(loaders, email)
        else Stakeholder(email=email, is_registered=False)
        for email in stakeholder_emails
    ]

    return tuple(stakeholders)


async def get_stakeholders_emails(
    loaders: Any, organization_id: str
) -> list[str]:
    org_stakeholders: tuple[Stakeholder, ...] = await get_stakeholders(
        loaders, organization_id
    )

    return [stakeholder.email for stakeholder in org_stakeholders]


async def has_group(
    loaders: Any, organization_id: str, group_name: str
) -> bool:
    try:
        group: Group = await loaders.group.load(group_name)
        return group.organization_id == organization_id
    except GroupNotFound:
        return False


async def has_access(loaders: Any, organization_id: str, email: str) -> bool:
    if (
        await authz.get_organization_level_role(email, organization_id)
        == "admin"
    ):
        return True

    try:
        organization_id = add_org_id_prefix(organization_id)
        await loaders.organization_access.load((organization_id, email))
        return True
    except StakeholderNotInOrganization:
        return False


async def invite_to_organization(
    loaders: Any,
    email: str,
    role: str,
    organization_name: str,
    modified_by: str,
) -> None:
    if validate_email_address(email) and validate_role_fluid_reqs(email, role):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        organization: Organization = await loaders.organization.load(
            organization_name
        )
        organization_id = organization.id
        url_token = token_utils.new_encoded_jwt(
            {
                "organization_id": organization_id,
                "user_email": email,
            },
        )
        await update_organization_access(
            organization_id,
            email,
            OrganizationAccessMetadataToUpdate(
                expiration_time=expiration_time,
                has_access=False,
                invitation=OrganizationInvitation(
                    is_used=False,
                    role=role,
                    url_token=url_token,
                ),
            ),
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
        schedule(
            groups_mail.send_mail_access_granted(
                loaders, mail_to, email_context
            )
        )


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


async def remove_credentials(
    loaders: Any, organization_id: str, credentials_id: str, modified_by: str
) -> None:
    organization: Organization = await loaders.organization.load(
        organization_id
    )
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
        and root.state.credential_id == credentials_id
    )
    await credentials_model.remove(
        credential_id=credentials_id,
        organization_id=organization_id,
    )


async def remove_user(
    loaders: Any, organization_id: str, email: str, modified_by: str
) -> bool:
    organization_id = add_org_id_prefix(organization_id)
    if not await has_access(loaders, organization_id, email):
        raise StakeholderNotInOrganization()

    await orgs_dal.remove(email=email, organization_id=organization_id)
    user_removed = await authz.revoke_organization_level_role(
        email, organization_id
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

    has_orgs = bool(await loaders.stakeholder_organizations_access.load(email))
    if not has_orgs:
        await stakeholders_domain.remove(email)
    user_credentials: tuple[
        Credentials, ...
    ] = await loaders.user_credentials.load(email)
    await collect(
        tuple(
            remove_credentials(
                loaders=loaders,
                organization_id=organization_id,
                credentials_id=credential.id,
                modified_by=modified_by,
            )
            for credential in user_credentials
        )
    )
    return user_removed and groups_removed


async def reject_register_for_organization_invitation(
    loaders: Any,
    organization_access: OrganizationAccess,
) -> bool:
    success: bool = False
    invitation = organization_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access.organization_id
    user_email = organization_access.email
    success = await remove_user(
        loaders, organization_id, user_email, user_email
    )
    return success


async def update_credentials(
    loaders: Any,
    attributes: CredentialAttributesToUpdate,
    credentials_id: str,
    organization_id: str,
    modified_by: str,
) -> None:
    current_credentials: Credentials = await loaders.credentials.load(
        CredentialsRequest(
            id=credentials_id,
            organization_id=organization_id,
        )
    )
    credentials_type = attributes.type or current_credentials.state.type
    credentials_name = attributes.name or current_credentials.state.name
    if (
        credentials_type is CredentialType.HTTPS
        and attributes.password is not None
        and attributes.user is None
    ):
        raise InvalidParameter("user")
    if (
        credentials_type is CredentialType.HTTPS
        and attributes.user is not None
        and attributes.password is None
    ):
        raise InvalidParameter("password")
    if current_credentials.state.name != credentials_name:
        await orgs_validations.validate_credentials_name_in_organization(
            loaders, organization_id, credentials_name
        )

    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret]
    if (
        credentials_type is CredentialType.HTTPS
        and attributes.token is not None
    ):
        secret = HttpsPatSecret(token=attributes.token)
    elif (
        credentials_type is CredentialType.HTTPS
        and attributes.user is not None
        and attributes.password is not None
    ):
        secret = HttpsSecret(
            user=attributes.user, password=attributes.password
        )
    elif credentials_type is CredentialType.SSH and attributes.key is not None:
        secret = SshSecret(
            key=orgs_utils.format_credentials_ssh_key(attributes.key)
        )
    else:
        secret = current_credentials.state.secret

    new_state = CredentialsState(
        modified_by=modified_by,
        modified_date=datetime_utils.get_iso_date(),
        name=credentials_name,
        secret=secret,
        type=credentials_type,
    )
    await credentials_model.update_credential_state(
        current_value=current_credentials.state,
        credential_id=credentials_id,
        organization_id=organization_id,
        state=new_state,
    )


async def update_organization_access(
    organization_id: str,
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
) -> None:
    return await orgs_dal.update_metadata(
        email=email, metadata=metadata, organization_id=organization_id
    )


async def update_invited_stakeholder(
    email: str,
    invitation: OrganizationInvitation,
    organization_id: str,
    role: str,
) -> None:
    if validate_role_fluid_reqs(email, role):
        invitation = invitation._replace(role=role)
        await update_organization_access(
            organization_id,
            email,
            OrganizationAccessMetadataToUpdate(invitation=invitation),
        )


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
    policies_to_update: PoliciesToUpdate,
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
        schedule(
            send_mail_policies(
                loaders=loaders,
                new_policies=policies_to_update._asdict(),
                organization_id=organization_id,
                organization_name=organization_name,
                responsible=user_email,
                date=today,
            )
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

    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = organization_data.policies._asdict().get(key)
        if val is not None and val != old_value:
            policies_content[POLICIES_FORMATTED[key]] = {
                "from": old_value,
                "to": val,
            }

    email_context: dict[str, Any] = {
        "entity_name": organization_name,
        "policies_link": f"{BASE_URL}/orgs/{organization_name}/policies",
        "policies_content": policies_content,
        "responsible": responsible,
        "date": datetime_utils.get_datetime_from_iso_str(date),
    }

    org_stakeholders: tuple[Stakeholder, ...] = await get_stakeholders(
        loaders, organization_id
    )

    stakeholders_emails = [
        stakeholder.email
        for stakeholder in org_stakeholders
        if await get_stakeholder_role(
            loaders,
            stakeholder.email,
            stakeholder.is_registered,
            organization_id,
        )
        in ["customer_manager", "user_manager"]
    ]

    if policies_content:
        await groups_mail.send_mail_updated_policies(
            loaders=loaders,
            email_to=stakeholders_emails,
            context=email_context,
        )


async def validate_acceptance_severity_range(
    loaders: Any, organization_id: str, values: PoliciesToUpdate
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
