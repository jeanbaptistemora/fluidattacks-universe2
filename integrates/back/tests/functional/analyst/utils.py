# Standard libraries
from typing import (
    Any,
    Dict,
    Optional
)

# Local libraries
from back.tests.functional.utils import get_graphql_result
from dataloaders import Dataloaders


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = 'integratesanalyst@fluidattacks.com',
    session_jwt: str = None,
    context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    result = await get_graphql_result(
        data,
        stakeholder,
        session_jwt,
        context
    )

    return result
