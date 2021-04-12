# Standard libraries

# Third-party libraries
from aioextensions import collect

# Local libraries
from backend import authz
from backend.dal.helpers.dynamodb import async_delete_item
from backend.dal import session as session_dal
from backend.typing import DynamoDelete as DynamoDeleteType


# Constants
USER_TABLE: str = 'FI_users'


async def remove_stakeholder(email: str) -> bool:
    success = all(
        await collect([
            authz.revoke_user_level_role(email),
            async_delete_item(
                USER_TABLE,
                DynamoDeleteType(Key={'email': email.lower()})
            )
        ])
    )
    await session_dal.logout(email)
    return success


def is_fluid_staff(email: str) -> bool:
    return email.endswith('@fluidattacks.com')


async def is_manager(email: str, group_name: str) -> bool:
    role: str = await authz.get_group_level_role(email, group_name)

    return role == 'group_manager'
