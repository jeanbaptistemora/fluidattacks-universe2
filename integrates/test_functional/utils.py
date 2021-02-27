# Standard libraries
from typing import (
    Awaitable,
    Any,
    Dict,
    List,
    Optional,
)

# Third party libraries
from aioextensions import (
    collect,
)
from ariadne import (
    graphql,
)

# Local libraries
from backend.api import (
    apply_context_attrs,
    get_new_context,
    Dataloaders
)
from backend.api.schema import (
    SCHEMA,
)
from backend.dal import (
    organization as dal_organization,
    user as dal_user,
)
from backend.domain import (
    project as domain_group,
)
from backend.utils import (
    user as user_utils,
)
from test_unit.utils import (
    create_dummy_session,
)

async def populate_db(data: Dict[str, Any]) -> bool:
    success: bool = False
    keys: List[str, str] = data.keys()
    coroutines_policies: List[Awaitable[bool]] = []

    if 'users' in keys:
        coroutines_users: List[Awaitable[bool]] = []
        coroutines_users.extend([
            dal_user.create(
                user['email'],
                user,
            )
            for user in data['users']
        ])
        success = all(await collect(coroutines_users))

    if 'orgs' in keys:
        coroutines_orgs: List[Awaitable[bool]] = []
        coroutines_orgs.extend([
            dal_organization.create(
                org['name'],
            )
            for org in data['orgs']
        ])
        success = success and all(await collect(coroutines_orgs))

        coroutines_org_users: List[Awaitable[bool]] = []
        for org in data['orgs']:
            for user in org['users']:
                coroutines_org_users.append(
                    dal_organization.add_user(
                        (await dal_organization.get_by_name(
                            org['name'],
                            ['id'],
                        ))['id'],
                        user,
                    )
                )
        success = success and all(await collect(coroutines_org_users))

    if 'policies' in keys:
        coroutines_policies.extend([
            dal_user.put_subject_policy(
                dal_user.SubjectPolicy(
                    level=policy['level'],
                    subject=policy['subject'],
                    object=(
                        await dal_organization.get_by_name(
                            policy['object'],
                            ['id'],
                        ))['id'] \
                        if policy['level'] == 'organization' \
                        else policy['object'],
                    role=policy['role'],
                ),
            )
            for policy in data['policies']
        ])
    success = success and all(await collect(coroutines_policies))
    return success



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
