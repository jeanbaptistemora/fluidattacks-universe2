# pylint:disable=too-many-lines
from .utils import (
    get_organization,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs_deco,
)
import bugsnag
from collections.abc import (
    AsyncIterator,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidAuthorization,
    InvalidGitCredentials,
    InvalidInactivityPeriod,
    InvalidNumberAcceptances,
    InvalidOrganization,
    InvalidParameter,
    InvalidSeverity,
    InvalidVulnerabilityGracePeriod,
    OrganizationNotFound,
    StakeholderNotFound,
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
    organization_access as org_access_model,
    organization_finding_policies as policies_model,
    organizations as orgs_model,
    portfolios as portfolios_model,
    roots as roots_model,
)
from db_model.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
    MIN_INACTIVITY_PERIOD,
    POLICIES_FORMATTED,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    CredentialsState,
    HttpsPatSecret,
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
    SshSecret,
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
import logging
import logging.config
from mailer import (
    groups as groups_mail,
    organizations as orgs_mail,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
    validations as validations_utils,
)
from newutils.organization_access import (
    format_invitation_state,
)
from newutils.validations import (
    validate_email_address_deco,
    validate_field_length_deco,
    validate_include_lowercase_deco,
    validate_include_number_deco,
    validate_include_uppercase_deco,
    validate_sequence_deco,
    validate_space_field_deco,
    validate_start_letter_deco,
    validate_symbols_deco,
)
from organization_access import (
    domain as orgs_access,
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
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
import sys
from trials import (
    domain as trials_domain,
)
from typing import (
    Any,
)
import uuid

logging.config.dictConfig(LOGGING)

# Constants
EMAIL_INTEGRATES = "integrates@fluidattacks.com"
LOGGER = logging.getLogger(__name__)


async def get_credentials(
    loaders: Dataloaders, credentials_id: str, organization_id: str
) -> Credentials:
    credentials = await loaders.credentials.load(
        CredentialsRequest(
            id=credentials_id,
            organization_id=organization_id,
        )
    )
    if credentials is None:
        raise InvalidGitCredentials()

    return credentials


async def add_credentials(
    loaders: Dataloaders,
    attributes: CredentialAttributesToAdd,
    organization_id: str,
    modified_by: str,
) -> str:
    if attributes.type is CredentialType.SSH:
        secret: HttpsSecret | HttpsPatSecret | SshSecret = SshSecret(
            key=orgs_utils.format_credentials_ssh_key(attributes.key or "")
        )
    elif attributes.token is not None:
        token: str = attributes.token
        secret = create_pat_secret(token=token)
    else:
        user: str = attributes.user or ""
        password: str = attributes.password or ""
        secret = create_https_secret(user=user, password=password)

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


@validate_role_fluid_reqs_deco("email", "role")
async def add_stakeholder(
    loaders: Dataloaders, organization_id: str, email: str, role: str
) -> None:
    # Check for customer manager granting requirements
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


@validate_email_address_deco("email")
async def add_without_group(
    *,
    email: str,
    role: str,
    is_register_after_complete: bool = False,
) -> None:
    await stakeholders_domain.update(
        email=email,
        metadata=StakeholderMetadataToUpdate(
            enrolled=False,
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

    await add_stakeholder(
        loaders=loaders,
        organization_id=organization_id,
        email=email,
        role=role,
    )
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
            email=email,
            role="user",
            is_register_after_complete=True,
        )
    stakeholder = await loaders.stakeholder.load(email)
    if stakeholder and not stakeholder.enrolled:
        await stakeholders_domain.update(
            email=email,
            metadata=StakeholderMetadataToUpdate(enrolled=True),
        )


@validate_space_field_deco("user")
@validate_space_field_deco("password")
@validate_start_letter_deco("password")
@validate_include_number_deco("password")
@validate_include_lowercase_deco("password")
@validate_include_uppercase_deco("password")
@validate_sequence_deco("password")
@validate_field_length_deco("password", limit=40, is_greater_than_limit=True)
@validate_field_length_deco("password", limit=100, is_greater_than_limit=False)
@validate_symbols_deco("password")
def create_https_secret(*, user: str, password: str) -> HttpsSecret:

    return HttpsSecret(user=user, password=password)


@validate_space_field_deco("token")
def create_pat_secret(*, token: str) -> HttpsPatSecret:

    return HttpsPatSecret(token=token)


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

    if (
        access := await loaders.organization_access.load(
            OrganizationAccessRequest(
                organization_id=organization_id, email=user_email
            )
        )
    ) is None:
        raise StakeholderNotInOrganization()

    return access


async def get_all_groups(
    loaders: Dataloaders,
) -> list[Group]:
    groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        groups.extend(org_groups)

    return groups


async def get_all_group_names(
    loaders: Dataloaders,
) -> list[str]:
    groups = await get_all_groups(loaders)
    group_names = [group.name for group in groups]

    return group_names


async def get_all_active_groups(
    loaders: Dataloaders,
) -> list[Group]:
    active_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_active_groups = groups_utils.exclude_review_groups(
            groups_utils.filter_active_groups(org_groups)
        )
        active_groups.extend(org_active_groups)

    return active_groups


async def get_all_trial_groups(
    loaders: Dataloaders,
) -> list[Group]:
    trial_groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_trial_groups = groups_utils.filter_trial_groups(org_groups)
        trial_groups.extend(org_trial_groups)

    return trial_groups


async def get_all_active_group_names(
    loaders: Dataloaders,
) -> list[str]:
    active_groups = await get_all_active_groups(loaders)
    active_group_names = [group.name for group in active_groups]

    return active_group_names


async def get_all_deleted_groups(
    loaders: Dataloaders,
) -> list[Group]:
    deleted_groups: list[Group] = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        org_deleted_groups = groups_utils.filter_deleted_groups(org_groups)
        deleted_groups.extend(org_deleted_groups)

    return deleted_groups


async def get_group_names(
    loaders: Dataloaders, organization_id: str
) -> list[str]:
    org_groups = await loaders.organization_groups.load(organization_id)

    return [group.name for group in org_groups]


async def exists(loaders: Dataloaders, organization_name: str) -> bool:
    try:
        await get_organization(loaders, organization_name.lower().strip())
        return True
    except OrganizationNotFound:
        return False


@validate_field_length_deco(
    "organization_name", limit=3, is_greater_than_limit=True
)
@validate_field_length_deco(
    "organization_name", limit=10, is_greater_than_limit=False
)
async def add_organization(
    *,
    loaders: Dataloaders,
    organization_name: str,
    email: str,
    country: str,
) -> Organization:
    if await exists(loaders, organization_name):
        raise InvalidOrganization("Name taken")
    if not re.match(r"^[a-zA-Z]{4,10}$", organization_name):
        raise InvalidOrganization("Invalid name")

    in_trial = await trials_domain.in_trial(loaders, email)
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
            if validations_utils.is_fluid_staff(email)
            else "user_manager"
        )
        await add_stakeholder(
            loaders=loaders,
            organization_id=organization.id,
            email=email,
            role=user_role,
        )
    return organization


async def get_stakeholder_role(
    loaders: Dataloaders,
    email: str,
    is_registered: bool,
    organization_id: str,
) -> str:
    if (
        org_access := await loaders.organization_access.load(
            OrganizationAccessRequest(
                organization_id=organization_id, email=email
            )
        )
    ) is None:
        raise StakeholderNotInOrganization()

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
    stakeholders_access = await loaders.organization_stakeholders_access.load(
        organization_id
    )

    return [access.email for access in stakeholders_access]


async def get_stakeholders(
    loaders: Dataloaders,
    organization_id: str,
    user_email: str | None = None,
) -> list[Stakeholder]:
    emails = await get_stakeholders_emails(loaders, organization_id)
    stakeholders: list[Stakeholder] = []
    for email in emails:
        try:
            stakeholder = await stakeholders_domain.get_stakeholder(
                loaders, email, user_email
            )
            stakeholders.append(stakeholder)
        except StakeholderNotFound:
            if not validations_utils.is_fluid_staff(email):
                stakeholders.append(Stakeholder(email=email))
    return stakeholders


async def has_group(
    loaders: Dataloaders, organization_id: str, group_name: str
) -> bool:
    if group := await loaders.group.load(group_name):
        return group.organization_id == organization_id
    return False


@validate_email_address_deco("email")
@validate_role_fluid_reqs_deco("email", "role")
async def invite_to_organization(
    *,
    loaders: Dataloaders,
    email: str,
    role: str,
    organization_name: str,
    modified_by: str,
) -> None:
    expiration_time = datetime_utils.get_as_epoch(
        datetime_utils.get_now_plus_delta(weeks=1)
    )
    organization = await get_organization(loaders, organization_name)
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
    confirm_access_url = f"{BASE_URL}/confirm_access_organization/{url_token}"
    reject_access_url = f"{BASE_URL}/reject_access_organization/{url_token}"
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
        groups_mail.send_mail_access_granted(loaders, mail_to, email_context)
    )


async def iterate_organizations() -> AsyncIterator[Organization]:
    async for organization in orgs_model.iterate_organizations():
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield organization  # NOSONAR


async def iterate_organizations_and_groups(
    loaders: Dataloaders,
) -> AsyncIterator[tuple[str, str, list[str]]]:
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
    organization = await get_organization(loaders, organization_id)
    organization_roots = await loaders.organization_roots.load(
        organization.name
    )
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


async def reassign_stakeholder_credentials(
    *,
    loaders: Dataloaders,
    email: str,
    modified_by: str,
    organization_id: str,
    send_reassignment_email: bool = False,
) -> None:
    user_org_credentials: list[Credentials] = [
        credential
        for credential in await loaders.user_credentials.load(email)
        if credential.organization_id == organization_id
    ]
    if not user_org_credentials:
        return

    current_owner_role = await authz.get_organization_level_role(
        loaders, email, organization_id
    )
    org_stakeholders = await loaders.organization_stakeholders_access.load(
        organization_id
    )
    email_candidates_to_reassign = [
        org_access.email
        for org_access in org_stakeholders
        if email != org_access.email
        and not re.match(r"forces\..*@fluidattacks.com", org_access.email)
        and org_access.role == current_owner_role
    ]
    new_owner_email = (
        email_candidates_to_reassign[0]
        if email_candidates_to_reassign
        else EMAIL_INTEGRATES
    )
    await collect(
        tuple(
            credentials_model.update_credential_state(
                current_value=credentials.state,
                credential_id=credentials.id,
                organization_id=organization_id,
                state=credentials.state._replace(
                    modified_by=EMAIL_INTEGRATES,
                    modified_date=datetime_utils.get_utc_now(),
                ),
                force_update_owner=True,
                new_owner_email=new_owner_email,
            )
            for credentials in user_org_credentials
        ),
        workers=1,
    )
    if send_reassignment_email:
        schedule(
            send_mail_reassigned_credentials_owner(
                loaders=loaders,
                organization_id=organization_id,
                owner_email=email,
                owner_role=current_owner_role,
            )
        )
    LOGGER.info(
        "Credentials owner reassigned",
        extra={
            "extra": {
                "credentials_ids": [
                    credentials.id for credentials in user_org_credentials
                ],
                "email": email,
                "modified_by": modified_by,
                "new_owner": new_owner_email,
                "organization_id": organization_id,
                "organization_role": current_owner_role,
            }
        },
    )


async def remove_access(
    organization_id: str,
    email: str,
    modified_by: str,
    send_reassignment_email: bool = False,
) -> None:
    loaders: Dataloaders = get_new_context()
    if not await orgs_access.has_access(loaders, organization_id, email):
        raise StakeholderNotInOrganization()

    org_group_names = await get_group_names(loaders, organization_id)
    await collect(
        tuple(
            group_access_domain.remove_access(loaders, email, group)
            for group in org_group_names
        ),
        workers=1,
    )
    await reassign_stakeholder_credentials(
        loaders=loaders,
        email=email,
        modified_by=modified_by,
        organization_id=organization_id,
        send_reassignment_email=send_reassignment_email,
    )
    await org_access_model.remove(email=email, organization_id=organization_id)
    stakeholder = await loaders.stakeholder.load(email)
    LOGGER.info(
        "Stakeholder removed from organization",
        extra={
            "extra": {
                "email": email,
                "modified_by": modified_by,
                "organization_id": organization_id,
                "last_login_date": stakeholder.last_login_date
                if stakeholder
                else "",
                "last_api_token_use_date": stakeholder.last_api_token_use_date
                if stakeholder
                else None,
            }
        },
    )

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
    current_credentials = await get_credentials(
        loaders=loaders,
        credentials_id=credentials_id,
        organization_id=organization_id,
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
    secret: (
        HttpsSecret
        | HttpsPatSecret
        | OauthAzureSecret
        | OauthBitbucketSecret
        | OauthGithubSecret
        | OauthGitlabSecret
        | SshSecret
    )
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
        secret = create_https_secret(user=user, password=password)
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
    invitation = invitation._replace(role=role)
    await update_organization_access(
        organization_id,
        email,
        OrganizationAccessMetadataToUpdate(invitation=invitation),
    )


@validate_role_fluid_reqs_deco("user_email", "new_role")
async def update_stakeholder_role(
    loaders: Dataloaders,
    user_email: str,
    organization_id: str,
    organization_access: OrganizationAccess,
    new_role: str,
) -> None:
    if organization_access.invitation:
        await update_invited_stakeholder(
            user_email,
            organization_access.invitation,
            organization_id,
            new_role,
        )
        if organization_access.invitation.is_used:
            await authz.grant_organization_level_role(
                loaders, user_email, organization_id, new_role
            )
    else:
        # For some users without invitation
        await authz.grant_organization_level_role(
            loaders, user_email, organization_id, new_role
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
    organization_data = await get_organization(loaders, organization_id)
    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = organization_data.policies._asdict().get(key)
        if val is not None and val != old_value:
            policies_content[POLICIES_FORMATTED[key]] = {
                "from": old_value,
                "to": val,
            }
    if not policies_content:
        return

    email_context: dict[str, Any] = {
        "entity_name": organization_name,
        "policies_link": f"{BASE_URL}/orgs/{organization_name}/policies",
        "policies_content": policies_content,
        "responsible": responsible,
        "date": modified_date,
    }
    org_stakeholders = await get_stakeholders(loaders, organization_id)
    stakeholders_emails = [
        stakeholder.email
        for stakeholder in org_stakeholders
        if stakeholder
        and await get_stakeholder_role(
            loaders,
            stakeholder.email,
            stakeholder.is_registered,
            organization_id,
        )
        in ["customer_manager", "user_manager"]
    ]
    await groups_mail.send_mail_updated_policies(
        loaders=loaders,
        email_to=stakeholders_emails,
        context=email_context,
    )


async def send_mail_reassigned_credentials_owner(
    *,
    loaders: Dataloaders,
    organization_id: str,
    owner_email: str,
    owner_role: str,
) -> None:
    organization = await get_organization(loaders, organization_id)
    email_context: dict[str, Any] = {
        "user_email": owner_email,
        "user_role": owner_role,
        "organization_name": organization.name,
        "credentials_link": f"{BASE_URL}/orgs/{organization.name}/credentials",
    }
    org_stakeholders = await get_stakeholders(loaders, organization_id)
    stakeholders_emails = [
        stakeholder.email
        for stakeholder in org_stakeholders
        if stakeholder
        and await get_stakeholder_role(
            loaders,
            stakeholder.email,
            stakeholder.is_registered,
            organization_id,
        )
        in ["customer_manager", "user_manager"]
    ]
    await orgs_mail.send_mail_reassigned_credentials_owner(
        loaders=loaders,
        email_to=stakeholders_emails,
        context=email_context,
    )


async def validate_acceptance_severity_range(
    loaders: Dataloaders, organization_id: str, values: PoliciesToUpdate
) -> bool:
    success: bool = True
    organization_data = await get_organization(loaders, organization_id)
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


def validate_inactivity_period(value: int) -> bool:
    success: bool = True
    if value < MIN_INACTIVITY_PERIOD:
        raise InvalidInactivityPeriod()
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


@validate_space_field_deco("azure_organization")
def verify_azure_org(azure_organization: str) -> None:
    if not azure_organization:
        raise InvalidParameter("azure_organization")
