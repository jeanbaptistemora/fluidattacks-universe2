from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='integratesuser@gmail.com', session_jwt=None):
    """Get result for customeradmin role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result
