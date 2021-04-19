# Standard libraries

# Third-party libraries

# Local libraries
from backend import authz


def is_fluid_staff(email: str) -> bool:
    return email.endswith('@fluidattacks.com')


async def is_manager(email: str, group_name: str) -> bool:
    role: str = await authz.get_group_level_role(email, group_name)

    return role == 'group_manager'
