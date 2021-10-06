#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
This migration creates an organization attribute in every fi_users item
The organization field will have the id of the same
If the organization exists, it will be assigned to the user
It it does not exists, it will be created

Migration must be executed when the code that creates the organization in the
user creation is in production, so all possible users have an organization
"""

from asgiref.sync import (
    async_to_sync,
)
import bugsnag
import django  # noqa
from organizations import (
    dal as orgs_dal,
)
import os
from users import (
    dal as users_dal,
)
import uuid

django.setup()

STAGE: str = os.environ["STAGE"]


def log(message: str) -> None:
    print(message)
    if STAGE != "test":
        bugsnag.notify(Exception(message), severity="info")


def main() -> None:
    """
    Assign organization to every user
    """
    log("Starting migration 0009")
    all_users = users_dal.get_all(
        filter_exp=(
            "attribute_exists(company) and "
            "attribute_not_exists(organization)"
        ),
        data_attr="email,company",
    )

    if STAGE == "test":
        log("Organizations will be added as follows:")
        unique_orgs = {}

    for user in all_users:
        user_email = user.get("email")
        org_name = user.get("company").lower()
        org = async_to_sync(orgs_dal.get)(org_name)
        if STAGE == "test":
            log(f"---\nUser: {user_email}")
            if org:
                log(f'Added to existing org {org["name"]} with ID {org["id"]}')
            else:
                if org_name not in unique_orgs:
                    unique_orgs[org_name] = f"ORG#{uuid.uuid4()}"
                org = {"id": unique_orgs[org_name], "name": org_name}
                log(f'Creating new org {org["name"]} with ID {org["id"]}')
            log(f'pk: {org["id"]}\nsk: {org["name"]}')
        else:
            if not org:
                org = async_to_sync(orgs_dal.create)(org_name)
            success: bool = users_dal.update(
                data={"organization": org["id"]}, email=user_email
            )
            if success:
                log(f"Migration 0010: User {user_email} succesfully migrated")


if __name__ == "__main__":
    main()
