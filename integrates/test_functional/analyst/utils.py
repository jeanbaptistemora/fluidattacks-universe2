# Standard libraries
from typing import Optional

# Local libraries
from backend.api import Dataloaders
from test_functional.utils import get_graphql_result


async def get_result(
    data,
    stakeholder: str = 'integratesanalyst@fluidattacks.com',
    session_jwt: str = None,
    context: Optional[Dataloaders] = None
):
    result = await get_graphql_result(
        data,
        stakeholder,
        session_jwt,
        context
    )

    return result
