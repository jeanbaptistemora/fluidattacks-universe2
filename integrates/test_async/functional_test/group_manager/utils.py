from test_async.functional_test.utils import get_graphql_result

async def get_result(data, stakeholder='unittest2@fluidattacks.com'):
    """Get result for group_manager role."""
    result = await get_graphql_result(data, stakeholder)
    return result
