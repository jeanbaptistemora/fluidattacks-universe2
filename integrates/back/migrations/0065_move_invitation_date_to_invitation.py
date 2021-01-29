"""
This migration move the attribute invitation_date of project_access table
to the field invitation of the same table
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
from backend import authz
from backend.dal.helpers import dynamodb
from backend.domain import (
    project as group_domain,
)
from backend.typing import (
    ProjectAccess as ProjectAccessType,
)

TABLE_ACCESS_NAME = 'FI_project_access'


async def move_invitation_date_to_invitation(
    project_access: ProjectAccessType
) -> bool:
    invitation_date = project_access['invitation_date']
    user_email = project_access['user_email']
    group_name = project_access['project_name']
    responsibility = project_access['responsibility']
    is_used = project_access['has_access']
    group_role = await authz.get_group_level_role(user_email, group_name)
    url_token = 'unknown'
    new_invitation = {
        'date': invitation_date,
        'is_used': is_used,
        'responsibility': responsibility,
        'role': group_role,
        'url_token': url_token,
    }
    print('project_access')
    pprint(project_access)
    print('new_invitation')
    pprint(new_invitation)

    success = cast(bool, await group_domain.update_access(
        user_email,
        group_name,
        {
            'invitation': new_invitation,
            'invitation_date': None
        }
    ))

    return success


async def main() -> None:
    scan_attrs = {
        'FilterExpression': (
            Attr('invitation_date').exists()
        ),
    }
    project_accesses = await dynamodb.async_scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(await collect(
        [
            move_invitation_date_to_invitation(project_access)
            for project_access in project_accesses
        ],
        workers=64
    ))

    print(f'Success: {success}')



if __name__ == '__main__':
    run(main())
