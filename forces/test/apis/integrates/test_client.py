from forces.apis.integrates.client import (
    ApiError,
    execute,
    session,
)
import pytest


@pytest.mark.asyncio
async def test_session(test_token: str, test_group: str) -> None:
    async with session(api_token=test_token) as client:
        query = """
            query ForcesDoTestGetGroup($name: String!){
                group(groupName: $name){
                    name
                }
            }
            """
        response = await client.execute(
            query,
            variables={"name": test_group},
            operation="ForcesDoTestGetGroup",
        )
        result = (await response.json()).get("data")
        assert result["group"]["name"] == test_group


@pytest.mark.asyncio
async def test_session_bad_query(test_token: str, test_group: str) -> None:
    query = """
            query ForcesDoTestGetGroup($name: String!){
                groupss(groupName: $name){
                    name
                }
            }
            """
    try:
        await execute(
            query,
            variables={"name": test_group},
            operation_name="ForcesDoTestGetGroup",
            api_token=test_token,
        )
    except ApiError as exc:
        assert exc.messages
        assert "Cannot query field" in exc.messages[0]


@pytest.mark.asyncio
async def test_session_bad_token(test_group: str) -> None:
    query = """
            query ForcesDoTestGetGroup($name: String!){
                group(groupName: $name){
                    name
                }
            }
            """

    try:
        await execute(
            query,
            variables={"name": test_group},
            operation_name="ForcesDoTestGetGroup",
            api_token="bad_token",
        )
    except ApiError as exc:
        assert "Login required" in exc.messages
