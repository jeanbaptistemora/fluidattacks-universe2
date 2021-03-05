# Standard libraries
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
from ariadne import graphql

# Local libraries
from back.tests.unit.utils import create_dummy_session
from backend.api import (
    apply_context_attrs,
    get_new_context,
    Dataloaders
)
from backend.api.schema import SCHEMA
from backend.domain import project as domain_group
from newutils import user as user_utils


async def complete_register(
    email: str,
    group_name: str,
):
    project_access = await domain_group.get_user_access(email, group_name)
    success = await user_utils.complete_register_for_group_invitation(
        project_access
    )

    return success


async def get_graphql_result(
    data: Dict[str, Any],
    stakeholder: str,
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    """Get graphql result."""
    request = await create_dummy_session(stakeholder, session_jwt)
    request = apply_context_attrs(
      request,
      loaders=context if context else get_new_context()
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
