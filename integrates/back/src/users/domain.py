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
    SecureAccessException,
)
from custom_types import (
    Invitation as InvitationType,
    Stakeholder as StakeholderType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
    User as UserType,
)
from datetime import (
    datetime,
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
    validate_phone_field,
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
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Awaitable,
    cast,
    Dict,
    List,
    Union,
)
from users import (
    dal as users_dal,
)


async def acknowledge_concurrent_session(email: str) -> bool:
    """Acknowledge termination of concurrent session"""
    return await users_dal.update(email, {"is_concurrent_session": False})


async def add_phone_to_user(email: str, phone: str) -> bool:
    """Update user phone number."""
    return await users_dal.update(email, {"phone": phone})


async def add_push_token(user_email: str, push_token: str) -> bool:
    if not re.match(r"^ExponentPushToken\[[a-zA-Z\d_-]+\]$", push_token):
        raise InvalidPushToken()

    user_attrs: dict = await get_attributes(user_email, ["push_tokens"])
    tokens: List[str] = user_attrs.get("push_tokens", [])
    if push_token not in tokens:
        return await users_dal.update(
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
        await users_dal.update(email, {"is_concurrent_session": True})
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
        raise SecureAccessException()


async def create(email: str, data: UserType) -> bool:
    return await users_dal.create(email, data)


async def delete(email: str) -> bool:
    success = all(
        await collect(
            [
                authz.revoke_user_level_role(email),
                users_dal.delete(email),
            ]
        )
    )
    await redis_del_by_deps("session_logout", session_email=email)
    return success


async def update_user_information(
    context: Any, modified_user_data: Dict[str, str], group_name: str
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    email = modified_user_data["email"]
    phone = modified_user_data["phone_number"]
    responsibility = modified_user_data["responsibility"]
    success: bool = False

    if responsibility:
        if len(responsibility) <= 50:
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

    if phone and validate_phone_field(phone):
        coroutines.append(add_phone_to_user(email, phone))
    else:
        logs_utils.cloudwatch_log(
            context,
            f"Security: {email} Attempted to edit "
            f"user phone bypassing validation",
        )

    if coroutines:
        success = all(await collect(coroutines))
    return success


async def ensure_user_exists(email: str) -> bool:
    return bool(await users_dal.get(email))


def get_invitation_state(
    invitation: InvitationType, stakeholder: StakeholderType
) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not stakeholder.get("is_registered", False):
        return "UNREGISTERED"
    return "CONFIRMED"


async def format_stakeholder(email: str, group_name: str) -> StakeholderType:
    group_access, stakeholder = await collect(
        (
            group_access_domain.get_user_access(email, group_name),
            get_by_email(email),
        )
    )
    invitation = cast(InvitationType, group_access.get("invitation"))
    invitation_state = get_invitation_state(invitation, stakeholder)
    if invitation_state == "PENDING":
        responsibility = invitation["responsibility"]
        group_role = invitation["role"]
        phone_number = invitation["phone_number"]
    else:
        responsibility = cast(str, group_access.get("responsibility", ""))
        group_role = await authz.get_group_level_role(email, group_name)
        phone_number = cast(str, stakeholder["phone_number"])
    return {
        **stakeholder,
        "responsibility": responsibility,
        "invitation_state": invitation_state,
        "phone_number": phone_number,
        "role": group_role,
    }


async def get(email: str) -> UserType:
    return await users_dal.get(email)


async def get_attributes(email: str, data: List[str]) -> UserType:
    """Get attributes of a user."""
    return await users_dal.get_attributes(email, data)


async def get_by_email(email: str) -> UserType:
    stakeholder_data: UserType = {
        "email": email,
        "first_login": "",
        "first_name": "",
        "last_login": "",
        "last_name": "",
        "legal_remember": False,
        "phone_number": "-",
        "push_tokens": [],
        "is_registered": True,
    }
    user: UserType = await users_dal.get(email)
    if user:
        stakeholder_data.update(
            {
                "email": user["email"],
                "first_login": user.get("date_joined", ""),
                "first_name": user.get("first_name", ""),
                "last_login": user.get("last_login", ""),
                "last_name": user.get("last_name", ""),
                "legal_remember": user.get("legal_remember", False),
                "phone_number": user.get("phone", "-"),
                "push_tokens": user.get("push_tokens", []),
            }
        )
    else:
        stakeholder_data.update({"is_registered": False})
    return stakeholder_data


async def get_data(email: str, attr: str) -> Union[str, UserType]:
    # pylint: disable=unsubscriptable-object
    data_attr = await get_attributes(email, [attr])
    if data_attr and attr in data_attr:
        return cast(UserType, data_attr[attr])
    return str()


async def get_stakeholders(
    group_name: str,
) -> List[StakeholderType]:
    group_stakeholders_emails = cast(
        List[str],
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
        List[StakeholderType],
        await collect(
            format_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        ),
    )
    return group_stakeholders


async def get_user_name(mail: str) -> Dict[str, UserType]:
    return {mail: await get_attributes(mail, ["last_name", "first_name"])}


async def has_valid_access_token(
    email: str, context: Dict[str, str], jti: str
) -> bool:
    """Verify if has active access token and match."""
    access_token = cast(Dict[str, str], await get_data(email, "access_token"))
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
    return await users_dal.update(email, {"registered": True})


async def remove_access_token(email: str) -> bool:
    """Remove access token attribute"""
    return await users_dal.update(email, {"access_token": None})


async def remove_push_token(user_email: str, push_token: str) -> bool:
    user_attrs: dict = await get_attributes(user_email, ["push_tokens"])
    tokens: List[str] = list(
        filter(
            lambda token: token != push_token,
            user_attrs.get("push_tokens", []),
        )
    )
    return await users_dal.update(user_email, {"push_tokens": tokens})


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
        success = await users_dal.update(email, {"access_token": access_token})
    else:
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(
        success=success, session_jwt=session_jwt
    )


async def update_legal_remember(email: str, remember: bool) -> bool:
    """Remember legal notice acceptance"""
    return await users_dal.update(email, {"legal_remember": remember})


async def update_last_login(email: str) -> bool:
    return await users_dal.update(
        str(email), {"last_login": datetime_utils.get_now_as_str()}
    )


async def update_invited_stakeholder(
    updated_data: Dict[str, str], invitation: InvitationType, group_name: str
) -> bool:
    success = False
    email = updated_data["email"]
    responsibility = updated_data["responsibility"]
    phone_number = updated_data["phone_number"]
    role = updated_data["role"]
    new_invitation = invitation.copy()
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_phone_field(phone_number)
        and validate_email_address(email)
        and await authz.validate_fluidattacks_staff_on_group(
            group_name, email, role
        )
    ):
        validate_role_fluid_reqs(email, role)
        new_invitation["phone_number"] = phone_number
        new_invitation["responsibility"] = responsibility
        new_invitation["role"] = role
        success = await group_access_domain.update(
            email,
            group_name,
            {
                "invitation": new_invitation,
            },
        )
    return success


async def update_multiple_user_attributes(
    email: str, data_dict: UserType
) -> bool:
    return await users_dal.update(email, data_dict)
