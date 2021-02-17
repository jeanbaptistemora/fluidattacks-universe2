"""
This migration removes the date attribute for a group invitation
in the project access table
"""
# Standard library
from pprint import pprint
from typing import (
    cast,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import Attr

# Local libraries
from backend.dal.helpers import dynamodb
from backend.domain import (
    project as group_domain,
)
from backend.typing import (
    ProjectAccess as ProjectAccessType,
)

TABLE_ACCESS_NAME = 'FI_project_access'


async def remove_group_invitation_date(
    project_access: ProjectAccessType
) -> bool:
    success = True
    user_email = project_access['user_email']
    group_name = project_access['project_name']
    invitation = project_access['invitation']
    new_invitation = invitation.copy()

    if new_invitation.get('date'):
        del new_invitation['date']

    success = cast(bool, await group_domain.update_access(
        user_email,
        group_name,
        {
            'invitation': new_invitation
        }
    ))
    print('project_access')
    pprint(project_access)
    print('new_invitation')
    pprint(new_invitation)

    return success


async def main() -> None:
    scan_attrs = {
        'FilterExpression': (
            Attr('invitation').exists()
        ),
    }
    project_accesses = await dynamodb.async_scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(await collect(
        [
            remove_group_invitation_date(project_access)
            for project_access in project_accesses
        ],
        workers=64
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
