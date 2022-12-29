# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
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
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessRequest,
)
from groups import (
    domain as groups_domain,
)
from remove_stakeholder.domain import (
    complete_deletion,
    get_confirm_deletion,
    get_email_from_url_token,
)
from typing import (
    Any,
    Optional,
)


async def complete_register(
    email: str,
    group_name: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    group_access: GroupAccess = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    await groups_domain.complete_register_for_group_invitation(
        loaders, group_access
    )


async def confirm_deletion(
    *,
    loaders: Dataloaders,
    email: str,
) -> None:
    access_with_deletion = await get_confirm_deletion(
        loaders=loaders, email=email
    )
    if access_with_deletion and access_with_deletion.confirm_deletion:
        user_email: str = await get_email_from_url_token(
            loaders=loaders,
            url_token=access_with_deletion.confirm_deletion.url_token,
        )
    if user_email == email:
        await complete_deletion(email=user_email)


async def reject_register(
    email: str,
    group_name: str,
) -> bool:
    loaders = get_new_context()
    group_access = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    await groups_domain.reject_register_for_group_invitation(
        get_new_context(), group_access
    )

    return True


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
    data: dict[str, Any],
    stakeholder: str,
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None,
) -> dict[str, Any]:
    """Get graphql result."""
    request = await create_dummy_session(stakeholder, session_jwt)
    request = apply_context_attrs(  # type: ignore
        request,  # type: ignore
        loaders=context if context else get_new_context(),
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
