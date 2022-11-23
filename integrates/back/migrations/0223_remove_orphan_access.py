# type: ignore

# pylint: disable=invalid-name
"""
Remove FI_project_access access for groups
that doesn't longer exist to avoid
group_not_found exception

Execution Time:    2022-06-04 at 00:02:23 UTC
Finalization Time: 2022-06-04 at 00:05:42 UTC
"""

from aioextensions import (
    collect,
    run,
)
from authz.policy import (
    _delete_subject_policy,
    get_group_level_role_legacy,
    get_user_subject_policies_legacy,
)
from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from dynamodb import (
    operations_legacy,
)
from group_access.domain import (
    get_stakeholder_groups_names,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from stakeholders.domain import (
    remove,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")
USERS_TABLE = "FI_users"


async def _process_user(
    *,
    email: str,
    group_name: str,
    loaders: Dataloaders,
    user: dict[str, str],
) -> None:
    try:
        await loaders.group.load(group_name)
    except GroupNotFound as ex:
        group_role = await get_group_level_role_legacy(
            email,
            group_name,
        )
        LOGGER_CONSOLE.info(
            ex,
            extra={
                "extra": {
                    "email": email,
                    "group_name": group_name,
                    "user": user,
                    "role": group_role,
                }
            },
        )
        await collect(
            [
                _delete_subject_policy(email, group_name),
                remove(email),
            ]
        )


async def process_user(
    *,
    email: str,
    loaders: Dataloaders,
    progress: float,
    user: dict[str, str],
) -> None:
    active, inactive = await collect(
        (
            get_stakeholder_groups_names(loaders, email, active=True),
            get_stakeholder_groups_names(loaders, email, active=False),
        )
    )
    groups = [
        policy[1]
        for policy in await get_user_subject_policies_legacy(email)
        if policy[2] == "group"
    ]
    user_groups = set(active + inactive + groups)

    await collect(
        tuple(
            _process_user(
                email=email,
                group_name=group,
                loaders=loaders,
                user=user,
            )
            for group in user_groups
        ),
        workers=4,
    )

    LOGGER_CONSOLE.info(
        "User processed",
        extra={
            "extra": {
                "user": email,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    users = await operations_legacy.scan(USERS_TABLE, {})
    LOGGER_CONSOLE.info(
        "Users",
        extra={"extra": {"user_len": len(users)}},
    )

    await collect(
        tuple(
            process_user(
                email=user["email"],
                loaders=loaders,
                user=user,
                progress=count / len(users),
            )
            for count, user in enumerate(users)
        ),
        workers=4,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
