# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration deletes the fields company/organization from projects
and users, since now the organization table is used for those relations.

Execution Time:    2020-07-16 10:40:00 UTC-5
Finalization Time: 2020-07-16 10:53:00 UTC-5
"""
from aioextensions import (
    collect,
    in_thread,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
import bugsnag
from groups import (
    dal as groups_dal,
)
from more_itertools import (
    chunked,
)
import os
from stakeholders import (
    dal as stakeholders_dal,
)

STAGE: str = os.environ["STAGE"]


async def main() -> None:
    group_filter: Attr = (
        Attr("organization").exists() | Attr("companies").exists()
    )
    groups = await in_thread(groups_dal.get_all, group_filter, "project_name")
    user_filter: Attr = (
        Attr("organization").exists() | Attr("company").exists()
    )
    users = await in_thread(stakeholders_dal.get_all, user_filter, "email")

    if STAGE == "test":
        print("-----\n")
        for user in users:
            print(f'User {user["email"]} will be updated')
        print("-----\n")
        for group in groups:
            print(f'Group {group["project_name"]} will be updated')
    else:
        for group_chunk in chunked(groups, 40):
            await collect(
                in_thread(
                    groups_dal.update,
                    group["project_name"],
                    {"companies": None, "organization": None},
                )
                for group in group_chunk
            )

        for user_chunk in chunked(users, 40):
            await collect(
                in_thread(
                    stakeholders_dal.update,
                    user["email"],
                    {"company": None, "organization": None},
                )
                for user in user_chunk
            )


async def log(message: str) -> None:
    print(message)
    if STAGE != "test":
        await in_thread(bugsnag.notify, Exception(message), severity="info")


if __name__ == "__main__":
    run(main())
