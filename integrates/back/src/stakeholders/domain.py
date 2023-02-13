from aioextensions import (
    collect,
    schedule,
)
from authz.validations import (
    validate_fluidattacks_staff_on_group_deco,
    validate_role_fluid_reqs_deco,
)
from botocore.exceptions import (
    ClientError,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidExpirationTime,
    InvalidField,
    InvalidFieldLength,
    RequiredNewPhoneNumber,
    RequiredVerificationCode,
    SamePhoneNumber,
    StakeholderNotFound,
    UnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
    stakeholders as stakeholders_model,
    subscriptions as subscriptions_model,
    vulnerabilities as vulns_model,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupInvitation,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderState,
    StakeholderTours,
)
from group_access import (
    domain as group_access_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
)
from newutils.validations import (
    validate_alphanumeric_field_deco,
    validate_email_address_deco,
    validate_field_length_deco,
)
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from settings import (
    LOGGING,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from stakeholders.validations import (
    validate_phone,
)
from typing import (
    Any,
    Optional,
)
from verify import (
    operations as verify_operations,
)
from verify.enums import (
    Channel,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def get_stakeholder(loaders: Dataloaders, email: str) -> Stakeholder:
    stakeholder = await loaders.stakeholder.load(email)
    if not stakeholder:
        raise StakeholderNotFound()
    return stakeholder


async def acknowledge_concurrent_session(email: str) -> None:
    """Acknowledge termination of concurrent session."""
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            is_concurrent_session=False,
        ),
        email=email,
    )


async def remove(email: str) -> None:
    loaders: Dataloaders = get_new_context()
    subscriptions = await loaders.stakeholder_subscriptions.load(email)
    await collect(
        tuple(
            subscriptions_model.remove(
                entity=subscription.entity,
                subject=subscription.subject,
                email=email,
            )
            for subscription in subscriptions
        ),
        workers=8,
    )
    me_vulnerabilities = await loaders.me_vulnerabilities.load(email)
    await collect(
        tuple(
            vulns_model.update_assigned_index(
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=None,
            )
            for vulnerability in me_vulnerabilities
        ),
        workers=8,
    )
    me_drafts = await loaders.me_drafts.load(email)
    await collect(
        tuple(
            findings_model.update_me_draft_index(
                finding_id=draft.id,
                group_name=draft.group_name,
                user_email="",
            )
            for draft in me_drafts
        ),
        workers=8,
    )
    await stakeholders_model.remove(email=email)
    LOGGER.info(
        "Stakeholder removed from db",
        extra={"extra": {"email": email}},
    )


@validate_field_length_deco("responsibility", limit=50)
@validate_alphanumeric_field_deco("responsibility")
async def _update_information(
    *,
    context: Any,
    email: str,
    group_name: str,
    responsibility: str,
    role: Any,
) -> None:
    await group_access_domain.update(
        loaders=context.loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            responsibility=responsibility,
            role=role,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )


async def update_information(
    context: Any, modified_data: dict[str, str], group_name: str
) -> None:
    email = modified_data["email"]
    responsibility = modified_data["responsibility"]
    role = modified_data["role"]
    if responsibility:
        try:
            await _update_information(
                context=context,
                email=email,
                group_name=group_name,
                responsibility=responsibility,
                role=role,
            )
        except InvalidFieldLength as exc:
            logs_utils.cloudwatch_log(
                context,
                f"Security: {email} Attempted to add responsibility to "
                f"group {group_name} bypassing validation",
            )
            raise exc
        except InvalidField as exc:
            logs_utils.cloudwatch_log(
                context,
                f"Security: {email} Attempted to add responsibility to "
                f"group {group_name} bypassing validation",
            )
            raise exc


async def has_valid_access_token(
    loaders: Dataloaders, email: str, context: dict[str, str], jti: str
) -> bool:
    """Verify if has active access token and match."""
    if not await exists(loaders, email):
        return False
    stakeholder = await get_stakeholder(loaders, email)
    if context and stakeholder.access_token:
        if sessions_utils.validate_hash_token(stakeholder.access_token, jti):
            if is_fluid_staff(email) and email.lower().startswith("forces."):
                return True
            with suppress(UnavailabilityError, ClientError):
                schedule(
                    stakeholders_model.update_metadata(
                        metadata=StakeholderMetadataToUpdate(
                            last_api_token_use_date=(
                                datetime_utils.get_utc_now()
                            ),
                        ),
                        email=email,
                    )
                )
            return True
    return False


def is_fluid_staff(email: str) -> bool:
    return email.endswith("@fluidattacks.com")


async def register(email: str) -> None:
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(is_registered=True),
        email=email,
    )


async def remove_access_token(email: str) -> None:
    """Remove access token attribute"""
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            access_token=StakeholderAccessToken(
                iat=0,
                jti="",
                salt="",
            ),
        ),
        email=email,
    )


async def update_access_token(
    email: str, expiration_time: int, **kwargs_token: Any
) -> str:
    """Update access token"""
    token_data = sessions_utils.calculate_hash_token()
    session_jwt = ""

    if sessions_utils.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = sessions_domain.encode_token(
            expiration_time=expiration_time,
            payload={
                "user_email": email,
                "jti": token_data["jti"],
                "iat": iat,
                **kwargs_token,
            },
            subject="api_token",
            api=True,
        )
        access_token = StakeholderAccessToken(
            iat=iat,
            jti=token_data["jti_hashed"],
            salt=token_data["salt"],
        )
        await stakeholders_model.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                access_token=access_token,
            ),
            email=email,
        )
    else:
        raise InvalidExpirationTime()

    return session_jwt


async def update_legal_remember(email: str, remember: bool) -> None:
    """Remember legal notice acceptance."""
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            legal_remember=remember,
        ),
        email=email,
    )


async def update_last_login(email: str) -> None:
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            last_login_date=datetime_utils.get_utc_now(),
        ),
        email=email,
    )


async def update_notification_preferences(
    email: str, preferences: NotificationsPreferences
) -> None:
    await stakeholders_model.update_state(
        user_email=email,
        state=StakeholderState(
            notifications_preferences=preferences,
            modified_date=datetime_utils.get_utc_now(),
            modified_by=email.lower().strip(),
        ),
    )


@validate_field_length_deco("responsibility", limit=50)
@validate_alphanumeric_field_deco("responsibility")
@validate_email_address_deco("email")
@validate_role_fluid_reqs_deco("email", "role")
@validate_fluidattacks_staff_on_group_deco("group", "email", "role")
async def update_invited_stakeholder(
    *,
    loaders: Dataloaders,
    email: str,
    responsibility: str,
    role: str,
    invitation: GroupInvitation,
    group: Group,
) -> None:
    new_invitation = invitation._replace(
        responsibility=responsibility, role=role
    )
    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name=group.name,
        metadata=GroupAccessMetadataToUpdate(
            invitation=new_invitation,
            responsibility=responsibility,
            role=role,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )


async def update(*, email: str, metadata: StakeholderMetadataToUpdate) -> None:
    return await stakeholders_model.update_metadata(
        email=email, metadata=metadata
    )


async def update_mobile(
    email: str, new_phone: StakeholderPhone, verification_code: str
) -> None:
    """Update the stakeholder's phone number."""
    validate_phone(new_phone)
    await verify_operations.validate_mobile(
        phone_number=get_international_format_phone_number(new_phone)
    )
    country_code = await verify_operations.get_country_code(
        get_international_format_phone_number(new_phone)
    )
    await verify_operations.check_verification(
        phone_number=get_international_format_phone_number(new_phone),
        code=verification_code,
    )
    stakeholder_phone = StakeholderPhone(
        calling_country_code=new_phone.calling_country_code,
        country_code=country_code,
        national_number=new_phone.national_number,
    )
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            phone=stakeholder_phone,
        ),
        email=email,
    )


async def update_tours(email: str, tours: dict[str, bool]) -> None:
    """New stakeholder workflow acknowledgment."""
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            tours=StakeholderTours(
                new_group=tours["new_group"],
                new_root=tours["new_root"],
                new_risk_exposure=tours["new_risk_exposure"],
            ),
        ),
        email=email,
    )


async def verify(
    loaders: Dataloaders,
    email: str,
    new_phone: Optional[StakeholderPhone],
    verification_code: Optional[str],
) -> None:
    """Start a verification process using OTP"""
    stakeholder = await get_stakeholder(loaders, email)
    stakeholder_phone: Optional[StakeholderPhone] = stakeholder.phone
    phone_to_verify = stakeholder_phone if new_phone is None else new_phone
    if new_phone:
        validate_phone(new_phone)

    if not phone_to_verify:
        raise RequiredNewPhoneNumber()

    if (
        stakeholder_phone is not None
        and new_phone is not None
        and get_international_format_phone_number(stakeholder_phone)
        == get_international_format_phone_number(new_phone)
    ):
        raise SamePhoneNumber()

    if new_phone and phone_to_verify is new_phone:
        await verify_operations.validate_mobile(
            phone_number=get_international_format_phone_number(new_phone)
        )

    if phone_to_verify is new_phone and stakeholder_phone is not None:
        if verification_code is None:
            raise RequiredVerificationCode()

        await verify_operations.check_verification(
            phone_number=get_international_format_phone_number(
                stakeholder_phone
            ),
            code=verification_code,
        )

    await verify_operations.start_verification(
        phone_number=get_international_format_phone_number(phone_to_verify),
        channel=Channel.SMS,
    )


async def exists(loaders: Dataloaders, email: str) -> bool:
    if await loaders.stakeholder.load(email):
        return True
    return False
