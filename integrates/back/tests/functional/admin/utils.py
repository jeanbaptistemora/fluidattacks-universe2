# Standard libraries
from typing import (
    Any,
    Dict,
    Optional
)

# Local libraries
from backend.api import Dataloaders
from test_functional.utils import get_graphql_result


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesmanager@gmail.com',
    session_jwt: str = None,
    context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    """Get result for admin role."""
    result = await get_graphql_result(
        data,
        stakeholder,
        session_jwt,
        context
    )

    return result
