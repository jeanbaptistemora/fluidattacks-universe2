"""
This migration remove that project access for that user that
has not access to the group or is no pending to accept an invitation
"""
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

ACCESS_TABLE_NAME = 'FI_project_access'

async def main() -> None:
    scan_attrs = {
        'FilterExpression': (
            Attr('has_access').eq(False)
            & Attr('invitation').not_exists()
        ),
    }
    project_accesses = await dynamodb.async_scan(ACCESS_TABLE_NAME, scan_attrs)

    print('project_accesses')
    print(project_accesses)

    success = all(await collect(
        [
            group_domain.remove_access(
                project_access['user_email'],
                project_access['project_name']
            )
            for project_access in project_accesses
        ],
        workers=64
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
