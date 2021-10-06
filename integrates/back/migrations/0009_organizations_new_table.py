#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
This migration creates an organization attribute in every fi_projects item
The organization field will have the id of the same
If the organization exists, it will be assigned to the group
It it does not exists, it will be created

Migration must be executed when the code that creates the organization in the
group creation is in production, so all possible groups have an organization
"""

import bugsnag
from groups import (
    dal as groups_dal,
)
from organizations import (
    domain as orgs_domain,
)
import os
import uuid

STAGE: str = os.environ["STAGE"]


def log(message: str) -> None:
    print(message)
    bugsnag.notify(Exception(message), severity="info")


def main() -> None:
    """
    Assign organization to every group
    """
    log("Starting migration 0009")
    all_projects = groups_dal.get_all(
        filtering_exp=(
            "attribute_exists(companies) and "
            "attribute_not_exists(organization)"
        ),
        data_attr="project_name,companies",
    )

    if STAGE == "test":
        log("Organizations will be added as follows:")
        unique_orgs = {}

    for proj in all_projects:
        proj_name = proj.get("project_name")
        org_name = proj.get("companies")[0].lower()
        if STAGE == "test":
            log(f'---\nGroup: {proj.get("project_name")}')
            if org_name not in unique_orgs:
                unique_orgs[org_name] = uuid.uuid4()
            log(f"pk: ORG#{unique_orgs[org_name]}\n" "sk: {org_name}")
        else:
            org_dict = orgs_domain.get_or_add(org_name)
            success: bool = groups_dal.update(
                data={"organization": org_dict["id"]}, group_name=proj_name
            )
            if success:
                log(f"Migration 0009: Group {proj_name} succesfully migrated")


if __name__ == "__main__":
    main()
