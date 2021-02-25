# Standard libraries
from typing import (
    Any,
    Dict
)

# Local libraries
from test_functional.utils import get_graphql_result


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesuser@gmail.com',    
    session_jwt: str = None
) -> Dict[str, Any]:
    """Get result for customeradmin role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)

    return result
