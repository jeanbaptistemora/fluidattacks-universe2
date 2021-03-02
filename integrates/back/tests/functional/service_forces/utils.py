# Standard libraries
from typing import (
    Any,
    Dict
)

# Local libraries
from back.tests.functional.utils import get_graphql_result


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesserviceforces@gmail.com',
    session_jwt: str = None
) -> Dict[str, Any]:
    """Get result for service_forces role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)

    return result
