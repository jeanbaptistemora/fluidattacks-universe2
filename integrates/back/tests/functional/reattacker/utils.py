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
    stakeholder: str = "integratesreattacker@fluidattacks.com",
    session_jwt: Optional[str] = None,
) -> Dict[str, Any]:
    """Get result for reattacker role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)

    return result
