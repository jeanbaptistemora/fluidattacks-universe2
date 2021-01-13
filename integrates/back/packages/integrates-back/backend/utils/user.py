# Standard libraries
from typing import (
    Any,
    Awaitable,
    Dict,
    List
)

# Third party libraries
from aioextensions import collect

# Local libraries
from backend import util
from backend.domain import (
    project as project_domain,
    user as user_domain
)
from backend.utils.validations import validate_phone_field


async def _add_acess(
    responsibility: str,
    email: str,
    project_name: str,
    context: object
) -> bool:
    result = False
    if len(responsibility) <= 50:
        result = await project_domain.add_access(
            email,
            project_name,
            'responsibility',
            responsibility
        )
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to add responsibility to '
            f'project{project_name} bypassing validation'
        )

    return result


async def modify_user_information(
    context: Any,
    modified_user_data: Dict[str, str],
    project_name: str
) -> bool:
    success = False
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    coroutines: List[Awaitable[bool]] = []

    if responsibility:
        coroutines.append(_add_acess(
            responsibility,
            email,
            project_name,
            context
        ))

    if phone and validate_phone_field(phone):
        coroutines.append(
            user_domain.add_phone_to_user(email, phone)
        )
        success = all(await collect(coroutines))
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit '
            f'user phone bypassing validation'
        )

    return success
