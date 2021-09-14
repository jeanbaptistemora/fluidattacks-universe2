from forces.apis.integrates.client import (
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
