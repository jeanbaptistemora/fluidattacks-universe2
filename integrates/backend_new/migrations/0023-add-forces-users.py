#/usr/bin/env python3
#-.- coding: utf-8 -.-
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
from backend.dal.project import get_active_projects
from backend.domain.project import get_many_groups
from backend.api.resolvers import user
from backend.api.resolvers.user import _create_new_user
from backend.domain import (
    user as user_domain, )


async def main() -> None:
    projects = await get_active_projects()
    groups = await get_many_groups(projects)
    for group in groups:
        configuration = group.get('historic_configuration', [])
        if not configuration:
            continue
        if not configuration[-1].get('has_forces', False):
            continue
        group_name = group['project_name']
        success = False
        try:
            success = await _create_new_user(
                context=dict(),
                email=user_domain.format_forces_user_email(group_name),
                responsibility='Forces service user',
                role='service_forces',
                phone_number='',
                group=group_name)
        except ClientError:
            print(f'Could not create user for {group_name}')
        if success:
            print(f'User created successfully for {group_name}')


if __name__ == '__main__':
    run(main())
