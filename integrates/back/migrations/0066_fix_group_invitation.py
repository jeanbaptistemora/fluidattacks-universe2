"""
This migration aims to fix those invitations that were not updated because
it stores info in Redis instead of the project access table and remove
the invitations that can not be used

Execution Time:    2021-02-02 at 17:26:42 UTC-05
Finalization Time: 2021-02-02 at 17:26:53 UTC-05
"""
# Standard library
from pprint import pprint
from typing import cast

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import Attr

# Local libraries
from backend.typing import ProjectAccess as ProjectAccessType
from dynamodb import operations_legacy as dynamodb_ops
from group_access import domain as groups_access_domain



TABLE_ACCESS_NAME = 'FI_project_access'


async def fix_invitation(
    project_access: ProjectAccessType
) -> bool:
    success = True
    has_access = project_access['has_access']
    invitation = project_access['invitation']
    user_email = project_access['user_email']
    group_name = project_access['project_name']

    if has_access and not invitation['is_used']:
        new_invitation = invitation.copy()
        new_invitation['is_used'] = True
        success = cast(bool, await groups_access_domain.update(
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
    elif (
        not has_access
        and not invitation['is_used']
        and invitation['url_token'] == 'unknown'
    ):
        success = cast(bool, await groups_access_domain.update(
            user_email,
            group_name,
            {
                'invitation': None
            }
        ))
        print('project_access')
        pprint(project_access)
        print('Invitation was removed')

    return success


async def main() -> None:
    scan_attrs = {
        'FilterExpression': (
            Attr('invitation').exists()
        ),
    }
    project_accesses = await dynamodb_ops.scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(await collect(
        [
            fix_invitation(project_access)
            for project_access in project_accesses
        ],
        workers=64
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
