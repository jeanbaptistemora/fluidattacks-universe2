# Third party libraries
import pytest

# Local libraries
from forces.apis.integrates.client import (
    session,
)


@pytest.mark.asyncio
async def test_session(test_token: str, test_group: str) -> None:
    async with session(api_token=test_token) as client:
        query = """
            query ForcesDoTestGetGroup($name: String!){
                project(projectName: $name){
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
        assert result["project"]["name"] == test_group
