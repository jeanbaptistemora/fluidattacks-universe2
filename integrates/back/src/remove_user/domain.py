from aioextensions import (
    collect,
)
from organizations.domain import (
    get_user_organizations,
    remove_user,
)
from remove_user.dal import (
    remove_stakeholder,
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
