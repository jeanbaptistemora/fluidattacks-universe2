from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='integratescloser@fluidattacks.com', session_jwt=None):
    """Get result for closer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result
