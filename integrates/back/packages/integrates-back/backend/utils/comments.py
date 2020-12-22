from collections import defaultdict
from backend import authz
from backend.exceptions import (
    InvalidCommentParent,
    PermissionDenied,
)


async def validate_handle_comment_scope(
    content: str,
    user_email: str,
    project_name: str,
    parent: str,
    context_store: defaultdict = None,
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
