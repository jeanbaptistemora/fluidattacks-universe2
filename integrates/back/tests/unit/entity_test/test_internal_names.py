# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
import pytest


@pytest.mark.asyncio
async def test_internal_group() -> None:
    """Check for internal group"""
    query = """{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }"""
    data = {"query": query}
    request = await create_dummy_session("integratesuser2@gmail.com")
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "internalNames" in result["data"]
