from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='integratesserviceforces@gmail.com', session_jwt=None):
    """Get result for service_forces role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result
