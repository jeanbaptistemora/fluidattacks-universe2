# Standard
from typing import Dict

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz, util
from backend.decorators import require_login
from backend.domain import project as group_domain, user as stakeholder_domain
from backend.exceptions import StakeholderNotFound
from backend.typing import Stakeholder


async def _resolve_for_organization(org_id: str, email: str) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholder_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(email, org_id)

    if org_role:
        return {
            **stakeholder,
            'responsibility': '',
            'role': org_role
        }

    raise StakeholderNotFound()


async def _resolve_for_group(group_name: str, email: str) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholder_domain.get_by_email(email)
    group_role: str = await authz.get_group_level_role(email, group_name)

    if group_role:
        access: Dict[str, str] = await group_domain.get_user_access(
            email,
            group_name
        )

        return {
            **stakeholder,
            'responsibility': access.get('responsibility', ''),
            'role': group_role
        }

    raise StakeholderNotFound()


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Stakeholder:
    entity: str = kwargs['entity']
    email: str = kwargs['user_email']

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    if entity == 'ORGANIZATION' and 'organization_id' in kwargs:
        org_id: str = kwargs['organization_id'].lower()

        if await authz.get_organization_level_role(user_email, org_id):
            return await _resolve_for_organization(org_id, email)

    if entity == 'PROJECT' and 'project_name' in kwargs:
        group_name: str = kwargs['project_name'].lower()

        if await authz.get_group_level_role(user_email, group_name):
            return await _resolve_for_group(group_name, email)

    raise StakeholderNotFound()
