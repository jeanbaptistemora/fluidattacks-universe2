# Standard libraries
from typing import (
    Any,
    DefaultDict,
    Dict,
)

# Third-party libraries

# Local libraries
from backend import (
    authz,
    util,
)
from backend.typing import Comment as CommentType
from custom_exceptions import (
    InvalidCommentParent,
    PermissionDenied,
)


async def _get_fullname(
    group_name: str,
    requester_email: str,
    objective_data: Dict[str, str]
) -> str:
    objective_email = objective_data['email']
    objective_possible_fullname = objective_data.get('fullname', '')
    real_name = objective_possible_fullname or objective_email
    is_requester_at_fluid: bool = '@fluidattacks.com' in requester_email
    is_objective_at_fluid: bool = '@fluidattacks.com' in objective_email

    # Only Fluid Attacks' staff is masked
    if is_requester_at_fluid or not is_objective_at_fluid:
        name_to_show = real_name
    else:
        objective_role = await authz.get_group_level_role(
            objective_email,
            group_name
        )
        name_to_show = {
            'analyst': 'Hacker at Fluid Attacks',
            'admin': 'Hacker at Fluid Attacks',
            'customeradmin': real_name,
        }.get(objective_role, 'Someone at Fluid Attacks')
    return name_to_show


async def fill_comment_data(
    group_name: str,
    requester_email: str,
    data: Dict[str, str]
) -> CommentType:
    fullname = await _get_fullname(
        group_name=group_name,
        requester_email=requester_email,
        objective_data=data
    )
    return {
        'content': data['content'],
        'created': util.format_comment_date(data['created']),
        'email': data['email'],
        'fullname': fullname if fullname else data['email'],
        'id': int(data['user_id']),
        'modified': util.format_comment_date(data['modified']),
        'parent': int(data['parent'])
    }


async def validate_handle_comment_scope(
    content: str,
    user_email: str,
    project_name: str,
    parent: str,
    context_store: DefaultDict[Any, Any] = DefaultDict(str),
) -> None:
    enforcer = await authz.get_group_level_enforcer(
        user_email,
        context_store
    )
    if content.strip() in {'#external', '#internal'}:
        if not enforcer(project_name, 'handle_comment_scope'):
            raise PermissionDenied()
        if parent == '0':
            raise InvalidCommentParent()
