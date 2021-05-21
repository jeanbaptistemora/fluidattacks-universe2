#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration creates force users.

Execution Time: 2020-08-13 13:32:00 UTC-5
Finalization Time: 2020-00-13 13:47:00 UTC-5
"""
# Standard library

# Third library
from aioextensions import run
from botocore.exceptions import ClientError

# Local library
from dataloaders import get_new_context
from groups.dal import get_active_groups
from groups.domain import get_many_groups
from forces.domain import create_forces_user


async def main() -> None:
    projects = await get_active_groups()
    groups = await get_many_groups(projects)
    for group in groups:
        configuration = group.get("historic_configuration", [])
        if not configuration:
            continue
        if not configuration[-1].get("has_forces", False):
            continue
        group_name = group["project_name"]
        success = False
        try:
            context = get_new_context()
            success = await create_forces_user(
                info=context, group_name=group_name
            )
        except ClientError:
            print(f"Could not create user for {group_name}")
        if success:
            print(f"User created successfully for {group_name}")


if __name__ == "__main__":
    run(main())
