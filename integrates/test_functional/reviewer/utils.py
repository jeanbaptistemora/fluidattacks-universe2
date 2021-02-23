from test_functional.utils import get_graphql_result

async def get_result(data, stakeholder='integratesreviewer@fluidattacks.com', session_jwt=None):
    """Get result for reviewer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result
