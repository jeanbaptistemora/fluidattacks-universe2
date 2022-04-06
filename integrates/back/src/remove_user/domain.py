from aioextensions import (
    collect,
    schedule,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAuthorization,
)
from custom_types import (
    MailContent,
)
from group_access.dal import (
    get_access_by_url_token,
    get_user_access,
    remove_access as remove_confirm_deletion,
    update,
)
from groups.domain import (
    get_groups_by_user,
)
from jose import (
    JWTError,
)
from mailer.common import (
    send_mail_confirm_deletion,
)
from newutils.datetime import (
    get_as_epoch,
    get_now_plus_delta,
)
from newutils.token import (
    decode_jwt,
    new_encoded_jwt,
)
from newutils.validations import (
    validate_email_address,
)
from organizations.domain import (
    get_user_organizations,
    remove_user,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from remove_user.dal import (
    remove_stakeholder,
)
from sessions.dal import (
    remove_session_key,
)
from subscriptions.domain import (
    get_user_subscriptions,
    unsubscribe_user_to_entity_report,
)
from typing import (
    Any,
)
from users.domain import (
    delete,
)


async def remove_user_all_organizations(*, loaders: Any, email: str) -> None:
    organizations_ids = await get_user_organizations(email)
    await collect(
        tuple(
            remove_user(loaders, organization_id, email)
            for organization_id in organizations_ids
        )
    )

    subscriptions = await get_user_subscriptions(user_email=email)
    await collect(
        tuple(
            unsubscribe_user_to_entity_report(
                report_entity=subscription["sk"]["entity"],
                report_subject=subscription["sk"]["subject"],
                user_email=email,
            )
            for subscription in subscriptions
        )
    )

    await collect(
        (
            delete(email),
            remove_stakeholder(user_email=email),
        )
    )
    await delete(email)


async def complete_deletion(*, loaders: Any, user_email: str) -> None:
    await collect(
        (
            remove_user_all_organizations(loaders=loaders, email=user_email),
            remove_confirm_deletion(user_email, "confirm_deletion"),
        )
    )
    stakeholder_organizations_ids = await get_user_organizations(user_email)
    stakeholder_groups = await get_groups_by_user(user_email)

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_organization_access",
                organization_id=organization_id,
            )
            for organization_id in stakeholder_organizations_ids
        )
    )

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_access",
                group_name=group_name,
            )
            for group_name in stakeholder_groups
        )
    )

    await collect(
        [
            remove_session_key(user_email, "jti"),
            remove_session_key(user_email, "web"),
            remove_session_key(user_email, "jwt"),
        ]
    )


async def get_email_from_url_token(
    *,
    url_token: str,
) -> str:
    try:
        token_content = decode_jwt(url_token)
        user_email: str = token_content["user_email"]
        if await get_access_by_url_token(url_token, attr="confirm_deletion"):
            return user_email
    except JWTError as ex:
        raise InvalidAuthorization() from ex

    return ""


async def get_confirm_deletion(
    *,
    email: str,
) -> dict[str, Any]:

    confirm_deletion = await get_user_access(email, "confirm_deletion")

    return confirm_deletion[0] if confirm_deletion else {}


async def confirm_deletion_mail(
    *,
    email: str,
) -> bool:
    success = False
    expiration_time = get_as_epoch(get_now_plus_delta(weeks=1))
    url_token = new_encoded_jwt(
        {
            "user_email": email,
        },
    )
    if validate_email_address(email):
        success = await update(
            email,
            "confirm_deletion",
            {
                "expiration_time": expiration_time,
                "confirm_deletion": {
                    "is_used": False,
                    "url_token": url_token,
                },
            },
        )
        confirm_access_url = f"{BASE_URL}/confirm_deletion/{url_token}"
        mail_to = [email]
        email_context: MailContent = {
            "email": email,
            "confirm_deletion_url": confirm_access_url,
        }
        schedule(send_mail_confirm_deletion(mail_to, email_context))

    return success
