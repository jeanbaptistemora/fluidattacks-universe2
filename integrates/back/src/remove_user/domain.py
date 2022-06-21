from aioextensions import (
    collect,
    schedule,
)
from authz.policy import (
    _get_user_subject_policies,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAuthorization,
    UnableToSendMail,
)
from decorators import (
    retry_on_exceptions,
)
from group_access.dal import (
    get_access_by_url_token,
    get_user_access,
    get_user_groups,
    remove_access as remove_confirm_deletion,
    update,
)
from group_access.domain import (
    remove_access,
)
from groups.domain import (
    get_groups_by_user,
)
from jose import (
    JWTError,
)
from jwcrypto.jwe import (
    JWException,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
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

mail_confirm_deletion = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_confirm_deletion)


async def remove_user_all_organizations(
    *, loaders: Any, email: str, modified_by: str
) -> None:
    organizations_ids = await get_user_organizations(email)
    await collect(
        tuple(
            remove_user(loaders, organization_id, email, modified_by)
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
            remove_stakeholder(stakeholder_email=email),
        )
    )

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_organization_access",
                organization_id=organization_id,
            )
            for organization_id in organizations_ids
        )
    )

    active, inactive = await collect(
        [
            get_user_groups(email, active=True),
            get_user_groups(email, active=False),
        ]
    )
    authz_groups = [
        policy[1] for policy in await _get_user_subject_policies(email)
    ]
    user_groups = set(active + inactive + authz_groups)
    await collect(
        tuple(remove_access(loaders, email, group) for group in user_groups)
    )


async def complete_deletion(*, loaders: Any, user_email: str) -> None:
    await collect(
        (
            remove_user_all_organizations(
                loaders=loaders,
                email=user_email,
                modified_by=user_email,
            ),
            remove_confirm_deletion(user_email, "confirm_deletion"),
        )
    )

    await collect(
        [
            remove_session_key(user_email, "jti"),
            remove_session_key(user_email, "web"),
            remove_session_key(user_email, "jwt"),
        ]
    )

    stakeholder_groups = await get_groups_by_user(loaders, user_email)

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_access",
                group_name=group_name,
            )
            for group_name in stakeholder_groups
        )
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
    except (JWTError, JWException) as ex:
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
        email_context: dict[str, Any] = {
            "email": email,
            "confirm_deletion_url": confirm_access_url,
            "empty_notification_notice": True,
        }
        schedule(mail_confirm_deletion(mail_to, email_context))

    return success
