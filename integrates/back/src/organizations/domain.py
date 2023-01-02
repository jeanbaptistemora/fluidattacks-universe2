# pylint:disable=too-many-lines
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
    TrialRestriction,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as credentials_model,
    enrollment as enrollment_model,
    organization_access as org_access_model,
    organization_finding_policies as policies_model,
    organizations as orgs_model,
    portfolios as portfolios_model,
    roots as roots_model,
)
from db_model.companies.types import (
    Company,
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
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.enums import (
    CredentialType,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.enums import (
    OrganizationInvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
    OrganizationAccessRequest,
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
from db_model.organizations.utils import (
    add_org_id_prefix,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
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
from jwcrypto.jwt import (
    JWTExpired,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
)
from newutils.organization_access import (
    format_invitation_state,
)
from newutils.validations import (
    validate_email_address,
    validate_field_length,
    validate_include_lowercase,
    validate_include_number,
    validate_include_uppercase,
    validate_sequence,
    validate_space_field,
    validate_start_letter,
    validate_symbols,
)
from organizations import (
    utils as orgs_utils,
    validations as orgs_validations,
)
from organizations.types import (
    CredentialAttributesToAdd,
    CredentialAttributesToUpdate,
)
import re
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)
import sys
from typing import (
    Any,
    AsyncIterator,
    Optional,
    Union,
)
import uuid

# Constants
DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")


async def add_credentials(
    loaders: Dataloaders,
    attributes: CredentialAttributesToAdd,
    organization_id: str,
    modified_by: str,
) -> str:
    if attributes.type is CredentialType.SSH:
        secret: Union[HttpsSecret, HttpsPatSecret, SshSecret] = SshSecret(
            key=orgs_utils.format_credentials_ssh_key(attributes.key or "")
        )
    elif attributes.token is not None:
        token: str = attributes.token
        validate_space_field(token)
        secret = HttpsPatSecret(token=token)
    else:
        user: str = attributes.user or ""
        password: str = attributes.password or ""
        validate_space_field(user)
        validate_space_field(password)
        validate_start_letter(password)
        validate_include_number(password)
        validate_include_lowercase(password)
        validate_include_uppercase(password)
        validate_sequence(password)
        validate_field_length(
            password,
            limit=40,
            is_greater_than_limit=True,
        )
        validate_field_length(
            password,
            limit=100,
            is_greater_than_limit=False,
        )
        validate_symbols(password)
        secret = HttpsSecret(
            user=user,
            password=password,
        )

    credential = Credentials(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=modified_by,
        state=CredentialsState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            name=attributes.name,
            secret=secret,
            type=attributes.type,
            is_pat=bool(attributes.is_pat),
            azure_organization=attributes.azure_organization,
        ),
    )
    await orgs_validations.validate_credentials_name_in_organization(
        loaders, credential.organization_id, credential.state.name
    )
    await credentials_model.add(credential=credential)

    return credential.id


async def add_group_access(
    loaders: Dataloaders, organization_id: str, group_name: str
) -> None:
    stakeholders = await get_stakeholders_emails(loaders, organization_id)
    stakeholders_roles = await collect(
        authz.get_organization_level_role(loaders, email, organization_id)
        for email in stakeholders
    )
    await collect(
        group_access_domain.add_access(
            loaders, stakeholder, group_name, "customer_manager"
        )
        for stakeholder, stakeholder_role in zip(
            stakeholders, stakeholders_roles
        )
        if stakeholder_role == "customer_manager"
    )


async def add_stakeholder(
    loaders: Dataloaders, organization_id: str, email: str, role: str
) -> None:
    # Check for customer manager granting requirements
    validate_role_fluid_reqs(email, role)
    await org_access_model.update_metadata(
        organization_id=organization_id,
        email=email,
        metadata=OrganizationAccessMetadataToUpdate(
            has_access=True,
        ),
    )
    await authz.grant_organization_level_role(
        loaders, email, organization_id, role
    )
    if role == "customer_manager":
        org_groups = await get_group_names(loaders, organization_id)
        await collect(
            group_access_domain.add_access(loaders, email, group, role)
            for group in org_groups
        )


async def add_without_group(
    email: str,
    role: str,
    is_register_after_complete: bool = False,
) -> None:
    if validate_email_address(email):
        await stakeholders_domain.update(
            email=email,
            metadata=StakeholderMetadataToUpdate(
                is_registered=is_register_after_complete,
            ),
        )
        await authz.grant_user_level_role(email, role)


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


async def complete_register_for_organization_invitation(
    loaders: Dataloaders, organization_access: OrganizationAccess
) -> None:
    invitation = organization_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access.organization_id
    email = organization_access.email
    if invitation:
        role = invitation.role
        updated_invitation = invitation._replace(is_used=True)

    await add_stakeholder(loaders, organization_id, email, role)
    await update_organization_access(
        organization_id,
        email,
        OrganizationAccessMetadataToUpdate(
            expiration_time=None,
            has_access=True,
            invitation=updated_invitation,
        ),
    )
    if not await stakeholders_domain.exists(loaders, email):
        await add_without_group(
            email,
            "user",
            is_register_after_complete=True,
        )
    enrollment: Enrollment = await loaders.enrollment.load(email)
    if not enrollment.enrolled:
        await enrollment_model.add(
            enrollment=Enrollment(
                email=email,
                enrolled=True,
            )
        )


async def get_access_by_url_token(
    loaders: Dataloaders,
    url_token: str,
) -> OrganizationAccess:
    try:
        token_content = sessions_domain.decode_token(url_token)
        organization_id: str = token_content["organization_id"]
        user_email: str = token_content["user_email"]
    except (KeyError, JWTExpired) as ex:
        raise InvalidAuthorization() from ex

    return await loaders.organization_access.load(
        OrganizationAccessRequest(
            organization_id=organization_id, email=user_email
        )
    )


async def get_all_groups(
    loaders: Dataloaders,
) -> tuple[Group, ...]:
    groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        groups.extend(org_groups)
    return tuple(groups)


async def get_all_group_names(
    loaders: Dataloaders,
) -> tuple[str, ...]:
    groups = await get_all_groups(loaders)
    group_names = tuple(group.name for group in groups)
    return group_names


async def get_all_active_groups(
    loaders: Dataloaders,
) -> tuple[Group, ...]:
    active_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_active_groups = list(
            groups_utils.exclude_review_groups(
                groups_utils.filter_active_groups(org_groups)
            )
        )
        active_groups.extend(org_active_groups)
    return tuple(active_groups)


async def get_all_trial_groups(
    loaders: Dataloaders,
) -> tuple[Group, ...]:
    trial_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_trial_groups = list(groups_utils.filter_trial_groups(org_groups))
        trial_groups.extend(org_trial_groups)
    return tuple(trial_groups)


async def get_all_active_group_names(
    loaders: Dataloaders,
) -> tuple[str, ...]:
    active_groups = await get_all_active_groups(loaders)
    active_group_names = tuple(group.name for group in active_groups)
    return active_group_names


async def get_all_deleted_groups(
    loaders: Dataloaders,
) -> tuple[Group, ...]:
    deleted_groups: list[Group] = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_deleted_groups = list(
            groups_utils.filter_deleted_groups(org_groups)
        )
        deleted_groups.extend(org_deleted_groups)
    return tuple(deleted_groups)


async def get_group_names(
    loaders: Dataloaders, organization_id: str
) -> tuple[str, ...]:
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization_id
    )
    return tuple(group.name for group in org_groups)


async def exists(loaders: Dataloaders, organization_name: str) -> bool:
    try:
        await loaders.organization.load(organization_name.lower().strip())
        return True
    except OrganizationNotFound:
        return False


async def add_organization(
    loaders: Dataloaders,
    organization_name: str,
    email: str,
    country: Optional[str],
) -> Organization:
    if await exists(loaders, organization_name):
        raise InvalidOrganization("Name taken")
    if not re.match(r"^[a-zA-Z]{4,10}$", organization_name):
        raise InvalidOrganization("Invalid name")

    company: Optional[Company] = await loaders.company.load(
        email.split("@")[1]
    )
    in_trial = company and not company.trial.completed
    if in_trial and await loaders.stakeholder_organizations_access.load(email):
        raise TrialRestriction()

    modified_date = datetime_utils.get_utc_now()
    organization = Organization(
        created_by=email,
        created_date=modified_date,
        country=country,
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
        user_role: str = (
            "customer_manager"
            if stakeholders_domain.is_fluid_staff(email)
            else "user_manager"
        )
        await add_stakeholder(loaders, organization.id, email, user_role)
    return organization


async def get_stakeholder_role(
    loaders: Dataloaders,
    email: str,
    is_registered: bool,
    organization_id: str,
) -> str:
    org_access: OrganizationAccess = await loaders.organization_access.load(
        OrganizationAccessRequest(organization_id=organization_id, email=email)
    )
    invitation_state = format_invitation_state(
        org_access.invitation, is_registered
    )

    return (
        org_access.invitation.role
        if org_access.invitation
        and invitation_state == OrganizationInvitiationState.PENDING
        else await authz.get_organization_level_role(
            loaders, email, organization_id
        )
    )


async def get_stakeholders_emails(
    loaders: Dataloaders, organization_id: str
) -> list[str]:
    stakeholders_access: tuple[
        OrganizationAccess, ...
    ] = await loaders.organization_stakeholders_access.load(organization_id)

    return [access.email for access in stakeholders_access]


async def get_stakeholders(
    loaders: Dataloaders, organization_id: str
) -> tuple[Stakeholder, ...]:
    emails = await get_stakeholders_emails(loaders, organization_id)

    return await loaders.stakeholder_with_fallback.load_many(emails)


async def has_group(
    loaders: Dataloaders, organization_id: str, group_name: str
) -> bool:
    try:
        group: Group = await loaders.group.load(group_name)
        return group.organization_id == organization_id
    except GroupNotFound:
        return False


async def has_access(
    loaders: Dataloaders, organization_id: str, email: str
) -> bool:
    if (
        await authz.get_organization_level_role(
            loaders, email, organization_id
        )
        == "admin"
    ):
        return True

    try:
        await loaders.organization_access.load(
            OrganizationAccessRequest(
                organization_id=organization_id, email=email
            )
        )
        return True
    except StakeholderNotInOrganization:
        return False


async def invite_to_organization(
    loaders: Dataloaders,
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
        url_token = sessions_domain.encode_token(
            expiration_time=expiration_time,
            payload={
                "organization_id": organization_id,
                "user_email": email,
            },
            subject="starlette_session",
        )
        await org_access_model.update_metadata(
            email=email,
            organization_id=organization_id,
            metadata=OrganizationAccessMetadataToUpdate(
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
        email_context: dict[str, Any] = {
            "admin": email,
            "group": organization_name,
            "responsible": modified_by,
            "confirm_access_url": confirm_access_url,
            "reject_access_url": reject_access_url,
            "user_role": role.replace("_", " "),
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
    loaders: Dataloaders,
) -> AsyncIterator[tuple[str, str, tuple[str, ...]]]:
    """Yield (org_id, org_name, org_group_names) non-concurrently generated."""
    async for organization in iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield organization.id, organization.name, await get_group_names(
            loaders, organization.id
        )  # NOSONAR


async def remove_credentials(
    loaders: Dataloaders,
    organization_id: str,
    credentials_id: str,
    modified_by: str,
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
                modified_date=datetime_utils.get_utc_now(),
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


async def remove_access(
    organization_id: str, email: str, modified_by: str
) -> None:
    loaders: Dataloaders = get_new_context()
    if not await has_access(loaders, organization_id, email):
        raise StakeholderNotInOrganization()

    org_group_names = await get_group_names(loaders, organization_id)
    await collect(
        tuple(
            group_access_domain.remove_access(loaders, email, group)
            for group in org_group_names
        )
    )
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
    await org_access_model.remove(email=email, organization_id=organization_id)

    loaders = get_new_context()
    has_orgs = bool(await loaders.stakeholder_organizations_access.load(email))
    if not has_orgs:
        await stakeholders_domain.remove(email)


async def remove_organization(
    *,
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    modified_by: str,
) -> None:
    await collect(
        remove_access(organization_id, email, modified_by)
        for email in await get_stakeholders_emails(loaders, organization_id)
    )
    # The state is updated to DELETED, prior to removal from db, as Streams
    # will archived this data for analytics purposes
    await orgs_model.update_state(
        organization_id=organization_id,
        organization_name=organization_name,
        state=OrganizationState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            status=OrganizationStateStatus.DELETED,
            pending_deletion_date=None,
        ),
    )
    await credentials_model.remove_organization_credentials(
        organization_id=organization_id
    )
    await policies_model.remove_org_finding_policies(
        organization_name=organization_name
    )
    await portfolios_model.remove_organization_portfolios(
        organization_name=organization_name
    )
    await orgs_model.remove(
        organization_id=organization_id, organization_name=organization_name
    )


async def reject_register_for_organization_invitation(
    organization_access: OrganizationAccess,
) -> None:
    invitation = organization_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access.organization_id
    user_email = organization_access.email
    await remove_access(organization_id, user_email, user_email)


async def update_credentials(
    loaders: Dataloaders,
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

    force_update_owner = False
    secret: Union[
        HttpsSecret,
        HttpsPatSecret,
        OauthBitbucketSecret,
        OauthGithubSecret,
        OauthGitlabSecret,
        SshSecret,
    ]
    if (
        credentials_type is CredentialType.HTTPS
        and attributes.token is not None
    ):
        secret = HttpsPatSecret(token=attributes.token)
        force_update_owner = True
    elif (
        credentials_type is CredentialType.HTTPS
        and attributes.user is not None
        and attributes.password is not None
    ):
        user: str = attributes.user
        password: str = attributes.password or ""
        validate_space_field(user)
        validate_space_field(password)
        validate_start_letter(password)
        validate_include_number(password)
        validate_include_lowercase(password)
        validate_include_uppercase(password)
        validate_sequence(password)
        validate_field_length(
            password,
            limit=40,
            is_greater_than_limit=True,
        )
        validate_field_length(
            password,
            limit=100,
            is_greater_than_limit=False,
        )
        validate_symbols(password)
        secret = HttpsSecret(user=user, password=password)
        force_update_owner = True
    elif credentials_type is CredentialType.SSH and attributes.key is not None:
        secret = SshSecret(
            key=orgs_utils.format_credentials_ssh_key(attributes.key)
        )
        force_update_owner = True
    else:
        secret = current_credentials.state.secret

    new_state = CredentialsState(
        modified_by=modified_by,
        modified_date=datetime_utils.get_utc_now(),
        name=credentials_name,
        secret=secret,
        is_pat=bool(attributes.is_pat),
        azure_organization=attributes.azure_organization,
        type=credentials_type,
    )
    await credentials_model.update_credential_state(
        current_value=current_credentials.state,
        credential_id=credentials_id,
        organization_id=organization_id,
        state=new_state,
        force_update_owner=force_update_owner,
    )


async def update_organization_access(
    organization_id: str,
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
) -> None:
    return await org_access_model.update_metadata(
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


async def update_url(
    organization_id: str,
    organization_name: str,
    vulnerabilities_url: str,
) -> None:
    await orgs_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            vulnerabilities_url=vulnerabilities_url
        ),
        organization_id=organization_id,
        organization_name=organization_name,
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
    loaders: Dataloaders,
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
        today = datetime_utils.get_utc_now()
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
                modified_date=today,
            )
        )


# pylint: disable=too-many-arguments
async def send_mail_policies(
    loaders: Dataloaders,
    new_policies: dict[str, Any],
    organization_id: str,
    organization_name: str,
    responsible: str,
    modified_date: datetime,
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
        "date": modified_date,
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
    loaders: Dataloaders, organization_id: str, values: PoliciesToUpdate
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
