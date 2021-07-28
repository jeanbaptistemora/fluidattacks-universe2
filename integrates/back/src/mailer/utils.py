from aioextensions import (
    collect,
)
from authz import (
    get_group_level_role,
)
from context import (
    FI_MAIL_REVIEWERS,
)
from group_access.domain import (
    get_users_to_notify,
)
from subscriptions.dal import (
    get_user_subscriptions,
)
from typing import (
    Any,
    List,
)


async def get_organization_name(loaders: Any, group_name: str) -> str:
    group_loader = loaders.group
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = loaders.organization
    organization = await organization_loader.load(org_id)
    return organization["name"]


async def is_user_subscribed_to_comments(
    *,
    user_email: str,
) -> bool:
    subscriptions = await get_user_subscriptions(user_email=user_email)
    sub_to_comments = [
        subscription
        for subscription in subscriptions
        if str(subscription["sk"]["entity"]).lower() == "comments"
    ]
    return len(sub_to_comments) > 0


async def _get_consult_users(
    *,
    group_name: str,
    comment_type: str,
) -> List[str]:
    recipients = FI_MAIL_REVIEWERS.split(",")
    users = await get_users_to_notify(group_name)
    if comment_type.lower() == "observation":
        roles: List[str] = await collect(
            [get_group_level_role(email, group_name) for email in users]
        )
        analysts = [
            email for email, role in zip(users, roles) if role == "analyst"
        ]

        return [*recipients, *analysts]

    return [*recipients, *users]


async def get_consult_users(
    *,
    group_name: str,
    comment_type: str,
) -> List[str]:
    recipients: List[str] = await _get_consult_users(
        group_name=group_name, comment_type=comment_type
    )
    are_users_subscribed: List[bool] = await collect(
        [
            is_user_subscribed_to_comments(user_email=recipient)
            for recipient in recipients
        ]
    )

    return [
        recipient
        for recipient, is_user_subscribed in zip(
            recipients, are_users_subscribed
        )
        if is_user_subscribed
    ]
