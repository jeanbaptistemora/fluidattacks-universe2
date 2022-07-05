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
from custom_types import (
    Phone,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
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
)
from group_access import (
    domain as group_access_domain,
)
from itertools import (
    chain,
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
    cast,
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
        stakeholder_email=email,
    )


async def add_push_token(
    loaders: Any, user_email: str, push_token: str
) -> bool:
    if not re.match(r"^ExponentPushToken\[[a-zA-Z\d_-]+\]$", push_token):
        raise InvalidPushToken()
    try:
        stakeholder: Optional[Stakeholder] = await loaders.stakeholder.load(
            user_email
        )
    except StakeholderNotFound:
        stakeholder = None
    if stakeholder and stakeholder.push_tokens:
        tokens: list[str] = stakeholder.push_tokens
    else:
        tokens = []
    if push_token not in tokens:
        return await stakeholders_dal.update(
            user_email, {"push_tokens": tokens + [push_token]}
        )
    return True


async def check_session_web_validity(request: Request) -> None:
    email: str = request.session["username"]
    session_key: str = request.session["session_key"]
    attr: str = "web"

    # Check if the user has a concurrent session and in case they do
    # raise the concurrent session modal flag
    if request.session.get("is_concurrent"):
        request.session.pop("is_concurrent")
        await stakeholders_dal.update(email, {"is_concurrent_session": True})
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


async def add(email: str, data: dict[str, Any]) -> bool:
    return await stakeholders_dal.add(email, data)


async def remove(email: str) -> bool:
    success = all(
        await collect(
            [
                authz.revoke_user_level_role(email),
                stakeholders_dal.remove(email),
            ]
        )
    )
    await redis_del_by_deps("session_logout", session_email=email)
    return success


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


async def ensure_exists(email: str) -> bool:
    return bool(await stakeholders_dal.get(email))


def get_invitation_state(
    invitation: dict[str, Any], stakeholder: dict[str, Any]
) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not stakeholder.get("is_registered", False):
        return "UNREGISTERED"
    return "CONFIRMED"


async def format_stakeholder(email: str, group_name: str) -> dict[str, Any]:
    group_access, stakeholder = await collect(
        (
            group_access_domain.get_user_access(email, group_name),
            get_by_email(email),
        )
    )
    invitation = group_access.get("invitation")
    invitation_state = get_invitation_state(invitation, stakeholder)
    if invitation_state == "PENDING":
        responsibility = invitation["responsibility"]
        group_role = invitation["role"]
    else:
        responsibility = cast(str, group_access.get("responsibility", ""))
        group_role = await authz.get_group_level_role(email, group_name)
    return {
        **stakeholder,
        "responsibility": responsibility,
        "invitation_state": invitation_state,
        "role": group_role,
    }


async def get(email: str) -> dict[str, Any]:
    return await stakeholders_dal.get(email)


async def get_attributes(email: str, data: list[str]) -> dict[str, Any]:
    """Get attributes of a user."""
    return await stakeholders_dal.get_attributes(email, data)


async def get_by_email(email: str) -> dict[str, Any]:
    stakeholder_data: dict[str, Any] = {
        "email": email,
        "date_joined": "",
        "first_name": "",
        "last_login": "",
        "last_name": "",
        "legal_remember": False,
        "phone": None,
        "push_tokens": [],
        "is_registered": True,
        "tours": {
            "new_group": False,
            "new_root": False,
        },
    }
    user: dict[str, Any] = await stakeholders_dal.get(email)
    if user:
        stakeholder_data.update(
            {
                "email": user["email"],
                "date_joined": user.get("date_joined", ""),
                "first_name": user.get("first_name", ""),
                "last_login": user.get("last_login", ""),
                "last_name": user.get("last_name", ""),
                "legal_remember": user.get("legal_remember", False),
                "phone": None
                if user.get("phone", None) is None
                else StakeholderPhone(
                    calling_country_code=user["phone"]["calling_country_code"],
                    country_code=user["phone"]["country_code"],
                    national_number=user["phone"]["national_number"],
                ),
                "push_tokens": user.get("push_tokens", []),
                "tours": stakeholder_data["tours"]
                if user.get("tours") is None
                else user["tours"],
            }
        )
    else:
        stakeholder_data.update({"is_registered": False})
    return stakeholder_data


async def get_data(email: str, attr: str) -> dict[str, Any]:
    data_attr = await get_attributes(email, [attr])
    if data_attr and attr in data_attr:
        return data_attr[attr]
    return {}


async def get_group_stakeholders(
    group_name: str,
) -> list[dict[str, Any]]:
    group_stakeholders_emails = cast(
        list[str],
        list(
            chain.from_iterable(
                await collect(
                    [
                        group_access_domain.get_group_users(group_name),
                        group_access_domain.get_group_users(group_name, False),
                    ]
                )
            )
        ),
    )
    group_stakeholders = cast(
        list[dict[str, Any]],
        await collect(
            tuple(
                format_stakeholder(email, group_name)
                for email in group_stakeholders_emails
            )
        ),
    )
    return group_stakeholders


async def get_name(mail: str) -> dict[str, dict[str, Any]]:
    return {mail: await get_attributes(mail, ["last_name", "first_name"])}


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


async def is_registered(email: str) -> bool:
    return bool(await get_data(email, "registered"))


async def register(email: str) -> bool:
    return await stakeholders_dal.update(email, {"registered": True})


async def remove_access_token(email: str) -> bool:
    """Remove access token attribute"""
    return await stakeholders_dal.update(email, {"access_token": None})


async def update_access_token(
    email: str, expiration_time: int, **kwargs_token: Any
) -> UpdateAccessTokenPayloadType:
    """Update access token"""
    token_data = token_utils.calculate_hash_token()
    session_jwt = ""
    success = False

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
        access_token = {
            "iat": iat,
            "jti": token_data["jti_hashed"],
            "salt": token_data["salt"],
        }
        success = await stakeholders_dal.update(
            email, {"access_token": access_token}
        )
    else:
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(
        success=success, session_jwt=session_jwt
    )


async def update_legal_remember(email: str, remember: bool) -> bool:
    """Remember legal notice acceptance"""
    return await stakeholders_dal.update(email, {"legal_remember": remember})


async def update_last_login(email: str) -> bool:
    return await stakeholders_dal.update(
        str(email), {"last_login": datetime_utils.get_now_as_str()}
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


async def update_attributes(email: str, data_dict: dict[str, Any]) -> bool:
    return await stakeholders_dal.update(email, data_dict)


async def update_mobile(
    email: str, new_phone: Phone, verification_code: str
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
    await stakeholders_dal.update(
        email, {"phone": stakeholder_phone._asdict()}
    )


async def update_tours(email: str, tours: dict[str, bool]) -> bool:
    """New user workflow acknowledgment"""
    return await stakeholders_dal.update(email, {"tours": tours})


async def verify(
    loaders: Any,
    email: str,
    new_phone: Optional[Phone],
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
