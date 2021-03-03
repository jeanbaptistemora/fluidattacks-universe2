# Standard libraries
from typing import (
    Any,
    Dict,
    Optional
)

# Local libraries
from backend.api import Dataloaders
from back.tests.functional.utils import get_graphql_result


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesreviewer@fluidattacks.com',
    session_jwt: str = None,
    context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    """Get result for reviewer role."""
    result = await get_graphql_result(
        data,
        stakeholder,
        session_jwt,
        context=context
    )

    return result
