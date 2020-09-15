from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='integratesmanager@gmail.com'):
    """Get result for admin role."""
    result = await get_graphql_result(data, stakeholder)
    return result
