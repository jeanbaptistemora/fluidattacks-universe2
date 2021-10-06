# pylint: disable=invalid-name
"""
This migration will clean IMAMURA from users
that already have another org.

Execution Time:    2020-12-01 at 14:41:39 UTC-05
Finalization Time: 2020-12-01 at 14:46:30 UTC-05
"""
from aioextensions import (
    collect,
)
from asyncio import (
    run,
)
import csv
from custom_exceptions import (
    UserNotInOrganization,
)
from organizations import (
    dal as orgs_dal,
    domain as orgs_domain,
)
import os
import time
from typing import (
    cast,
    List,
)

STAGE: str = os.environ["STAGE"]


async def remove_user_from_imamura(user: str, org_id: str) -> bool:
    try:
        success: bool = cast(bool, await orgs_domain.remove_user(org_id, user))
        if success:
            print(f"[INFO] User {user} removed from imamura")
        else:
            print(f"[ERROR] Failed to remove user {user} from imamura")
        return success
    except UserNotInOrganization:
        print(f"[INFO] User {user} already remove from imamura")
        return True


async def main() -> None:
    print("[INFO] Starting migration 0036")
    user_emails: List[str] = []
    org = await orgs_dal.get_by_name("imamura", ["id"])
    with open(
        "back/migrations/users.csv", newline="", encoding="utf8"
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "imamura" in row["Organizations"]:
                user_emails.append(row["email"])
    if STAGE == "test":
        for user in user_emails:
            print(
                f"[INFO] User {user} will be removed from org with id "
                f'{org["id"]}'
            )
    else:
        users_removed = await collect(
            remove_user_from_imamura(user, str(org["id"]))
            for user in user_emails
        )
        if False in list(users_removed):
            print("[INFO] Migration fails")
    print("[INFO] End migration 0036\n")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
