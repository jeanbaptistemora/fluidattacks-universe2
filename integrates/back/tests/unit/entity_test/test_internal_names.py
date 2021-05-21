import pytest

from ariadne import graphql

from api.schema import SCHEMA
from back.tests.unit.utils import create_dummy_session


@pytest.mark.asyncio
async def test_internal_project():
    """Check for internal project"""
    query = """{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }"""
    data = {"query": query}
    request = await create_dummy_session("integratescustomer@gmail.com")
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "internalNames" in result["data"]
