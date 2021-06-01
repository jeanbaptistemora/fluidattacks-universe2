from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    Dataloaders,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = "integratesuser@gmail.com",
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get result for customeradmin role."""
    result = await get_graphql_result(data, stakeholder, session_jwt, context)

    return result
