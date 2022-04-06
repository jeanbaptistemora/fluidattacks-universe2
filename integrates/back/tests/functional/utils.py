# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from batch.dal import (
    get_actions,
)
from batch.types import (
    BatchProcessing,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from remove_user.domain import (
    complete_deletion,
    get_confirm_deletion,
    get_email_from_url_token,
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


async def confirm_deletion(
    *,
    email: str,
) -> bool:
    deletion = await get_confirm_deletion(email=email)
    user_email: str = await get_email_from_url_token(
        url_token=deletion["confirm_deletion"]["url_token"]
    )
    if user_email == email:
        return await complete_deletion(
            loaders=get_new_context(), user_email=user_email
        )

    return False


async def reject_register(
    email: str,
    group_name: str,
) -> bool:
    group_access = await group_access_domain.get_user_access(email, group_name)
    redis_del_by_deps_soon(
        "reject_access",
        group_name=group_name,
    )
    success = await groups_domain.reject_register_for_group_invitation(
        get_new_context(), group_access
    )

    return success


async def get_batch_job(*, action_name: str, entity: str) -> BatchProcessing:
    all_actions = await get_actions()
    return next(
        (
            action
            for action in all_actions
            if action.entity == entity and action.action_name == action_name
        )
    )


async def get_graphql_result(
    data: Dict[str, Any],
    stakeholder: str,
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get graphql result."""
    request = await create_dummy_session(stakeholder, session_jwt)
    request = apply_context_attrs(
        request, loaders=context if context else get_new_context()
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
