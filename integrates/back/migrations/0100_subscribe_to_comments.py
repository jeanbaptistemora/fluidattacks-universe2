# pylint: disable=invalid-name
"""
Subscribe Fluid Attacks staff to "COMMENTS":
    https://gitlab.com/fluidattacks/product/-/issues/4972

Execution Time:    2021-07-14 at 12:05:28 UTC-05
Finalization Time: 2021-07-14 at 12:07:36 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from group_access.domain import (
    get_users_to_notify,
)
from groups.dal import (
    get_active_groups,
)
from itertools import (
    chain,
)
from subscriptions import (
    domain as subs_domain,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

PROD: bool = True


async def _get_subscriptions_to_comments() -> List[Dict[Any, Any]]:
    subs = await subs_domain.get_subscriptions_to_entity_report(
        audience="user",
    )
    return [sub for sub in subs if sub["sk"]["entity"] == "COMMENTS"]


async def main() -> None:
    groups = await get_active_groups()
    active_users = set(
        chain.from_iterable(
            await collect(get_users_to_notify(group) for group in groups)
        )
    )
    print(f"Active: {len(active_users)} users")

    fluid_users = [
        user for user in active_users if "@fluidattacks.com" in user
    ]
    print(f"Fluid: {len(fluid_users)} users")

    print(
        f"Subscriptions BEFORE migration: "
        f"{len(await _get_subscriptions_to_comments())}"
    )

    if PROD:
        await collect(
            subs_domain.subscribe_user_to_entity_report(
                event_frequency="DAILY",
                report_entity="COMMENTS",
                report_subject="ALL_GROUPS",
                user_email=user,
            )
            for user in fluid_users
        )

        print(
            f"Subscriptions AFTER migration: "
            f"{len(await _get_subscriptions_to_comments())}"
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
