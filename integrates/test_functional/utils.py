from ariadne import graphql

from backend.api import apply_context_attrs
from backend.api.schema import SCHEMA
from backend.domain import(
    project as group_domain,
)
from backend.utils import (
    user as user_utils,
)
from test_unit.utils import create_dummy_session


async def complete_register(
    email: str,
    group_name: str,
):
    project_access = await group_domain.get_user_access(email, group_name)
    success = await user_utils.complete_register_for_group_invitation(
        project_access
    )

    return success


async def get_graphql_result(data, stakeholder, session_jwt=None):
    """Get graphql result."""
    request = await create_dummy_session(stakeholder, session_jwt)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
