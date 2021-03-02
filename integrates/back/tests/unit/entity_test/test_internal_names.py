import pytest
from datetime import datetime, timedelta

from ariadne import graphql
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA
from back.tests.unit.utils import create_dummy_session


@pytest.mark.asyncio
async def test_internal_project():
    """Check for internal project"""
    query = '''{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }'''
    data = {'query': query}
    request = await create_dummy_session('integratescustomer@gmail.com')
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'internalNames' in result['data']
