# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    expiration_time: int,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateAccessToken(expirationTime: {expiration_time}) {{
                sessionJwt
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_me_data(
    *,
    user: str,
    session_jwt: str,
) -> dict:
    query: str = """
        query GetMeData {
            me {
                permissions
                role
            }
        }
    """
    data: dict = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
        session_jwt=session_jwt,
    )


async def get_me_access_token(
    *,
    user: str,
) -> dict:
    query: str = """
        query GetMeData {
            me {
                accessToken
            }
        }
    """
    data: dict = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
