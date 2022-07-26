from aioextensions import (
    collect,
    schedule,
)
from authz.policy import (
    get_user_subject_policies,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAuthorization,
    UnableToSendMail,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    dal as group_access_dal,
    domain as group_access_domain,
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
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from sessions.dal import (
    remove_session_key,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from subscriptions.domain import (
    get_user_subscriptions,
    unsubscribe_user_to_entity_report,
)
from typing import (
    Any,
)

mail_confirm_deletion = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_confirm_deletion)


async def remove_stakeholder_all_organizations(
    *, loaders: Any, email: str, modified_by: str
) -> None:
    organizations: tuple[
        OrganizationAccess, ...
    ] = await loaders.stakeholder_organizations_access.load(email)

    organizations_ids: list[str] = [
        org.organization_id for org in organizations
    ]
    await collect(
        tuple(
            orgs_domain.remove_access(
                loaders, organization_id, email, modified_by
            )
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

    await stakeholders_domain.remove(email=email)
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
            group_access_dal.get_user_groups(email, active=True),
            group_access_dal.get_user_groups(email, active=False),
        ]
    )
    authz_groups = [
        policy[1] for policy in await get_user_subject_policies(email)
    ]
    user_groups = set(active + inactive + authz_groups)
    await collect(
        tuple(
            group_access_domain.remove_access(loaders, email, group)
            for group in user_groups
        )
    )


async def complete_deletion(*, loaders: Any, user_email: str) -> None:
    await collect(
        (
            remove_stakeholder_all_organizations(
                loaders=loaders,
                email=user_email,
                modified_by=user_email,
            ),
            group_access_dal.remove_access(user_email, "confirm_deletion"),
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
        if await group_access_dal.get_access_by_url_token(
            url_token, attr="confirm_deletion"
        ):
            return user_email
    except (JWTError, JWException) as ex:
        raise InvalidAuthorization() from ex

    return ""


async def get_confirm_deletion(
    *,
    email: str,
) -> dict[str, Any]:
    confirm_deletion = await group_access_dal.get_user_access(
        email, "confirm_deletion"
    )

    return confirm_deletion[0] if confirm_deletion else {}


async def confirm_deletion_mail(
    *,
    loaders: Any,
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
        success = await group_access_dal.update(
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
        schedule(mail_confirm_deletion(loaders, mail_to, email_context))

    return success
