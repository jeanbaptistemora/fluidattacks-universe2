# Standard libraries
from typing import (
    Any,
    Awaitable,
    cast,
    Dict,
    List,
)

# Third-party libraries
import bugsnag
from aioextensions import collect

# Local libraries
from backend import (
    authz,
    util,
)
from backend.dal import user as user_dal
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.domain import (
    organization as org_domain,
    project as group_domain,
)
from backend.typing import (
    Invitation as InvitationType,
    ProjectAccess as GroupAccessType,
    User as UserType,
)
from newutils import apm
from newutils.validations import (
    validate_email_address,
    validate_phone_field,
)
from users.domain import core as users_core
from __init__ import FI_DEFAULT_ORG


async def complete_register_for_group_invitation(
    group_access: GroupAccessType
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    invitation = cast(InvitationType, group_access['invitation'])
    if invitation['is_used']:
        bugsnag.notify(Exception('Token already used'), severity='warning')

    group_name = cast(str, group_access['project_name'])
    phone_number = cast(str, invitation['phone_number'])
    responsibility = cast(str, invitation['responsibility'])
    role = cast(str, invitation['role'])
    user_email = cast(str, group_access['user_email'])
    updated_invitation = invitation.copy()
    updated_invitation['is_used'] = True

    coroutines.extend([
        group_domain.update_access(
            user_email,
            group_name,
            {
                'expiration_time': None,
                'has_access': True,
                'invitation': updated_invitation,
                'responsibility': responsibility,
            }
        ),
        authz.grant_group_level_role(user_email, group_name, role)
    ])

    organization_id = await org_domain.get_id_for_group(group_name)
    if not await org_domain.has_user_access(organization_id, user_email):
        coroutines.append(
            org_domain.add_user(organization_id, user_email, 'customer')
        )

    if await users_core.get_data(user_email, 'email'):
        coroutines.append(
            users_core.add_phone_to_user(user_email, phone_number)
        )
    else:
        coroutines.append(
            users_core.create(user_email, {'phone': phone_number})
        )

    if not await users_core.is_registered(user_email):
        coroutines.extend([
            users_core.register(user_email),
            authz.grant_user_level_role(user_email, 'customer')
        ])

    success = all(await collect(coroutines))
    if success:
        redis_del_by_deps_soon(
            'confirm_access',
            group_name=group_name,
            organization_id=organization_id,
        )
    return success


async def create_without_group(
    email: str,
    role: str,
    phone_number: str = ''
) -> bool:
    success = False
    if (
        validate_phone_field(phone_number) and
        validate_email_address(email)
    ):
        new_user_data: UserType = {}
        new_user_data['email'] = email
        new_user_data['authorized'] = True
        new_user_data['registered'] = True
        if phone_number:
            new_user_data['phone'] = phone_number

        success = all(
            await collect([
                authz.grant_user_level_role(email, role),
                users_core.create(email, new_user_data)
            ])
        )
        org = await org_domain.get_or_create(FI_DEFAULT_ORG, email)
        if not await org_domain.has_user_access(str(org['id']), email):
            await org_domain.add_user(str(org['id']), email, 'customer')
    return success


async def edit_user_information(
    context: Any,
    modified_user_data: Dict[str, str],
    group_name: str
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    email = modified_user_data['email']
    phone = modified_user_data['phone_number']
    responsibility = modified_user_data['responsibility']
    success: bool = False

    if responsibility:
        if len(responsibility) <= 50:
            coroutines.append(
                group_domain.update_access(
                    email,
                    group_name,
                    {'responsibility': responsibility}
                )
            )
        else:
            util.cloudwatch_log(
                context,
                f'Security: {email} Attempted to add responsibility to '
                f'project{group_name} bypassing validation'
            )

    if phone and validate_phone_field(phone):
        coroutines.append(users_core.add_phone_to_user(email, phone))
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit '
            f'user phone bypassing validation'
        )

    if coroutines:
        success = all(await collect(coroutines))
    return success


@apm.trace()
async def get_groups(
    user_email: str,
    active: bool = True,
    organization_id: str = ''
) -> List[str]:
    user_groups: List[str] = []
    groups = await user_dal.get_projects(user_email, active)
    group_level_roles = await authz.get_group_level_roles(user_email, groups)
    can_access_list = await collect(
        group_domain.can_user_access(group, role)
        for role, group in zip(group_level_roles.values(), groups)
    )
    user_groups = [
        group
        for can_access, group in zip(can_access_list, groups)
        if can_access
    ]

    if organization_id:
        org_groups = await org_domain.get_groups(organization_id)
        user_groups = [
            group
            for group in user_groups
            if group in org_groups
        ]
    return user_groups
