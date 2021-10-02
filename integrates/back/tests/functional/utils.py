from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def complete_register(
    email: str,
    group_name: str,
) -> bool:
    group_access = await group_access_domain.get_user_access(email, group_name)
    success = await groups_domain.complete_register_for_group_invitation(
        group_access
    )

    return success


async def get_graphql_result(
    data: Dict[str, Any],
    stakeholder: str,
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get graphql result."""
    # pylint: disable=unsubscriptable-object
    request = await create_dummy_session(stakeholder, session_jwt)
    request = apply_context_attrs(
        request, loaders=context if context else get_new_context()
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
