# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error,invalid-name
"""
This migration erases duplicate users from both DynamoDB and MySQL,
created by the Azure auth backend when it could not resolve the user correctly.

Execution Time: 2020-06-02 19:07 UTC-5
Finalization Time: 2020-06-02 19:12 UTC-5
"""
from boto3.dynamodb.conditions import (
    Attr,
)
import bugsnag
from django.contrib.auth.models import (
    User,
)
import os
from stakeholders.dal import (
    get_all as get_all_dynamo_users,
    remove as remove_dynamo_user,
)
from typing import (
    List,
)

PROVIDER = "azuread-tenant-oauth2"
STAGE: str = os.environ["STAGE"]


def delete_duplicated_users_dynamo() -> None:
    for user in get_all_dynamo_users(Attr("email").exists(), "email"):
        # Duplicated usernames have the syntax user@domain.comrandom_string
        if len(user["email"].split(".")[-1]) > 10:
            if STAGE == "test":
                print(f'User {user["email"]} will be deleted from DynamoDB...')
            else:
                remove_dynamo_user(email=user["email"])
                log(
                    f'Migration 0007: User {user["email"]} was deleted '
                    "from DynamoDB"
                )


def delete_duplicated_users_mysql() -> None:
    users_created_with_errors = []

    for user in User.objects.filter(social_auth__provider=PROVIDER):
        try:
            if "@" not in user.social_auth.get(provider=PROVIDER).uid:
                if len(user.username.split(".")[-1]) > 10:
                    if STAGE == "test":
                        print(
                            f"User {user.username} will be deleted from MySQL"
                        )
                    else:
                        user.delete()
                        log(
                            f"Migration 0007: User {user.username} was "
                            "deleted from MySQL"
                        )
                elif user.email not in users_created_with_errors:
                    users_created_with_errors.append(user.email)
        except AttributeError:
            log(f"Migration 0007: Special case found with user {user.email}")

    if users_created_with_errors:
        fix_users_created_with_errors(users_created_with_errors)


def fix_users_created_with_errors(email_list: List[str]) -> None:
    for email in email_list:
        users = User.objects.filter(email=email).order_by("id")
        if len(users) == 2:
            if STAGE == "test":
                print(f"User {users[1].username} will be deleted from MySQL")
                print(
                    f"User {users[0].username} uid will be updated from "
                    f"{users[0].social_auth.get(provider=PROVIDER).uid} to "
                    f"{email}"
                )
            else:
                users[1].delete()
                users[0].social_auth.update(uid=email)
                log(
                    f"Migration 0007: User {users[1].username} was deleted "
                    "from MySQL"
                )
                log(
                    f"Migration 0007: User {users[0].username} uid was be "
                    "updated from "
                    f"{users[0].social_auth.get(provider=PROVIDER).uid} to "
                    f"{email}"
                )
        else:
            print(f"Migration 0007: Special case for user with email {email}")


def log(message: str) -> None:
    if STAGE != "test":
        bugsnag.notify(Exception(message), severity="info")


def main() -> None:
    delete_duplicated_users_dynamo()
    delete_duplicated_users_mysql()
    log("Migration 0007: finished migration successfully")


if __name__ == "__main__":
    main()
