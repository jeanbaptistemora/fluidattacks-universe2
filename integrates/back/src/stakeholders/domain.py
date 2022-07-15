from aioextensions import (
    collect,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    ExpiredToken,
    InvalidExpirationTime,
    InvalidPushToken,
    RequiredNewPhoneNumber,
    RequiredVerificationCode,
    SamePhoneNumber,
    SecureAccessException,
    StakeholderNotFound,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderAccessToken,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderTours,
)
from group_access import (
    domain as group_access_domain,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    token as token_utils,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
)
import re
from redis_cluster.model import (
    KeyNotFound as RedisKeyNotFound,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from sessions import (
    dal as sessions_dal,
)
from stakeholders import (
    dal as stakeholders_dal,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from stakeholders.validations import (
    validate_phone,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Awaitable,
    Optional,
)
from verify import (
    operations as verify_operations,
)
from verify.enums import (
    Channel,
)


async def acknowledge_concurrent_session(email: str) -> None:
    """Acknowledge termination of concurrent session."""
    await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            is_concurrent_session=False,
        ),
        email=email,
    )


async def add_push_token(
    loaders: Any, user_email: str, push_token: str
) -> None:
    if not re.match(r"^ExponentPushToken\[[a-zA-Z\d_-]+\]$", push_token):
        raise InvalidPushToken()
    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    tokens: list[str] = stakeholder.push_tokens or []
    if push_token not in tokens:
        await stakeholders_dal.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                push_tokens=tokens + [push_token]
            ),
            email=user_email,
        )


async def check_session_web_validity(request: Request) -> None:
    email: str = request.session["username"]
    session_key: str = request.session["session_key"]
    attr: str = "web"

    # Check if the user has a concurrent session and in case they do
    # raise the concurrent session modal flag
    if request.session.get("is_concurrent"):
        request.session.pop("is_concurrent")
        await stakeholders_dal.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                is_concurrent_session=True,
            ),
            email=email,
        )
    try:
        # Check if the user has an active session but it's different
        # than the one in the cookie
        if await sessions_dal.get_session_key(email, attr) == session_key:
            # Session and cookie are ok and up to date
            pass
        else:
            # Session or the cookie are expired, let's logout the user
            await sessions_dal.remove_session_key(email, attr)
            request.session.clear()
            raise ExpiredToken()
    except RedisKeyNotFound:
        # User do not even has an active session
        raise SecureAccessException() from None


async def add(data: Stakeholder) -> None:
    return await stakeholders_dal.add(stakeholder=data)


async def remove(email: str) -> None:
    await authz.revoke_user_level_role(email)
    await stakeholders_dal.remove(email=email)
    await redis_del_by_deps("session_logout", session_email=email)
    return None


async def update_information(
    context: Any, modified_data: dict[str, str], group_name: str
) -> bool:
    coroutines: list[Awaitable[bool]] = []
    email = modified_data["email"]
    responsibility = modified_data["responsibility"]
    success: bool = False

    if responsibility:
        if validate_field_length(
            responsibility, 50
        ) and validate_alphanumeric_field(responsibility):
            coroutines.append(
                group_access_domain.update(
                    email, group_name, {"responsibility": responsibility}
                )
            )
        else:
            logs_utils.cloudwatch_log(
                context,
                f"Security: {email} Attempted to add responsibility to "
                f"group {group_name} bypassing validation",
            )

    if coroutines:
        success = all(await collect(coroutines))
    return success


async def has_valid_access_token(
    loaders: Any, email: str, context: dict[str, str], jti: str
) -> bool:
    """Verify if has active access token and match."""
    try:
        stakeholder: Optional[Stakeholder] = await loaders.stakeholder.load(
            email
        )
    except StakeholderNotFound:
        stakeholder = None
    access_token: Optional[StakeholderAccessToken] = (
        stakeholder.access_token if stakeholder else None
    )
    resp = False
    if context and access_token:
        resp = token_utils.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp


def is_fluid_staff(email: str) -> bool:
    return email.endswith("@fluidattacks.com")


async def register(email: str) -> None:
    await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(is_registered=True),
        email=email,
    )


async def remove_access_token(email: str) -> None:
    """Remove access token attribute"""
    await stakeholders_dal.update_metadata(
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
    token_data = token_utils.calculate_hash_token()
    session_jwt = ""

    if token_utils.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = token_utils.new_encoded_jwt(
            {
                "user_email": email,
                "jti": token_data["jti"],
                "iat": iat,
                "exp": expiration_time,
                "sub": "api_token",
                **kwargs_token,
            },
            api=True,
        )
        access_token = StakeholderAccessToken(
            iat=iat,
            jti=token_data["jti_hashed"],
            salt=token_data["salt"],
        )
        await stakeholders_dal.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                access_token=access_token,
            ),
            email=email,
        )
    else:
        raise InvalidExpirationTime()

    return session_jwt


async def update_legal_remember(email: str, remember: bool) -> None:
    """Remember legal notice acceptance"""
    return await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            legal_remember=remember,
        ),
        email=email,
    )


async def update_last_login(email: str) -> None:
    return await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            last_login_date=datetime_utils.get_iso_date(),
        ),
        email=email,
    )


async def update_invited_stakeholder(
    updated_data: dict[str, str],
    invitation: dict[str, Any],
    group: Group,
) -> bool:
    success = False
    email = updated_data["email"]
    responsibility = updated_data["responsibility"]
    role = updated_data["role"]
    new_invitation = invitation.copy()
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_email_address(email)
        and validate_role_fluid_reqs(email, role)
        and await authz.validate_fluidattacks_staff_on_group(
            group, email, role
        )
    ):
        new_invitation["responsibility"] = responsibility
        new_invitation["role"] = role
        success = await group_access_domain.update(
            email,
            group.name,
            {
                "invitation": new_invitation,
            },
        )
    return success


async def update_attributes(
    email: str, stakeholder_data: StakeholderMetadataToUpdate
) -> None:
    return await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            first_name=stakeholder_data.first_name,
            last_name=stakeholder_data.last_name,
            registration_date=stakeholder_data.registration_date,
            last_login_date=stakeholder_data.last_login_date,
        ),
        email=email,
    )


async def update_mobile(
    email: str, new_phone: StakeholderPhone, verification_code: str
) -> None:
    """Update the user's phone number"""
    validate_phone(new_phone)
    await verify_operations.validate_mobile(
        phone_number=get_international_format_phone_number(new_phone)
    )
    country_code = await verify_operations.get_contry_code(
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
    return await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            phone=stakeholder_phone,
        ),
        email=email,
    )


async def update_tours(email: str, tours: dict[str, bool]) -> None:
    """New user workflow acknowledgment"""
    return await stakeholders_dal.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            tours=StakeholderTours(
                new_group=tours["new_group"],
                new_root=tours["new_root"],
            ),
        ),
        email=email,
    )


async def verify(
    loaders: Any,
    email: str,
    new_phone: Optional[StakeholderPhone],
    verification_code: Optional[str],
) -> None:
    """Start a verification process using OTP"""
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    user_phone: Optional[StakeholderPhone] = stakeholder.phone
    phone_to_verify = user_phone if new_phone is None else new_phone
    if new_phone:
        validate_phone(new_phone)

    if not phone_to_verify:
        raise RequiredNewPhoneNumber()

    if (
        user_phone is not None
        and new_phone is not None
        and get_international_format_phone_number(user_phone)
        == get_international_format_phone_number(new_phone)
    ):
        raise SamePhoneNumber()

    if phone_to_verify is new_phone:
        await verify_operations.validate_mobile(
            phone_number=get_international_format_phone_number(new_phone)
        )

    if phone_to_verify is new_phone and user_phone is not None:
        if verification_code is None:
            raise RequiredVerificationCode()

        await verify_operations.check_verification(
            phone_number=get_international_format_phone_number(user_phone),
            code=verification_code,
        )

    await verify_operations.start_verification(
        phone_number=get_international_format_phone_number(phone_to_verify),
        channel=Channel.SMS,
    )
