# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
    create_dummy_session,
)
import pytest

pytestmark = pytest.mark.asyncio


async def test_user_list_groups() -> None:
    query = """
        query {
            listUserGroups(userEmail: "continuoushacking@gmail.com") {
                name
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert result["data"]["listUserGroups"][0]["name"] == "asgard"
