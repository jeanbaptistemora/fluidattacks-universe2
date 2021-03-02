# Standard libraries
from typing import (
    Any,
    Dict
)

# Local libraries
from back.tests.functional.utils import get_graphql_result


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesreviewer@fluidattacks.com',
    session_jwt: str = None
) -> Dict[str, Any]:
    """Get result for reviewer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)

    return result
