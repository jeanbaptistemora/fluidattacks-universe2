from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='integratesmanager@gmail.com', session_jwt=None):
    """Get result for admin role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result
