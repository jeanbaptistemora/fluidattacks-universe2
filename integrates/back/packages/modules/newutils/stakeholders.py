# Standard libraries
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union
)

# Third party libraries
from aioextensions import collect

# Local libraries
from backend import authz
from backend.dal import (
    session as session_dal,
    user as user_dal,
)


def check_enums(
    to_check: Dict[Union[int, str, Optional[str]], List[Callable[..., Any]]]
) -> None:
    for variable, callables in to_check.items():
        if variable:
            check_to_do = callables[0]
            exception = callables[1]
            try:
                if not check_to_do(variable):
                    raise exception()
            except ValueError:
                raise exception()


async def remove(email: str) -> bool:
    success = all(
        await collect([
            authz.revoke_user_level_role(email),
            user_dal.delete(email)
        ])
    )
    await session_dal.logout(email)

    return success
