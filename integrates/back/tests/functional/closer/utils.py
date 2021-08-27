from back.tests.functional.utils import (
    get_graphql_result,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = "integratescloser@fluidattacks.com",
    session_jwt: Optional[str] = None,
) -> Dict[str, Any]:
    """Get result for reattacker/closer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)

    return result
