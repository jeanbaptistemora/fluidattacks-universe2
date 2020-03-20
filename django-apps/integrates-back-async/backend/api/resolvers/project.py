# pylint: disable=import-error

from backend.decorators import (
    enforce_authz_async, require_login
)
from backend.domain import project as project_domain
from backend.services import get_user_role
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
def resolve_create_project(_, info, **kwargs):
    """Resolve create_project mutation."""
    user_data = util.get_jwt_content(info.context)
    user_role = get_user_role(user_data)
    success = project_domain.create_project(
        user_data['user_email'], user_role, **kwargs)
    if success:
        project = kwargs.get('project_name').lower()
        util.invalidate_cache(user_data['user_email'])
        util.cloudwatch_log(
            info.context,
            f'Security: Created project {project} successfully')
    return dict(success=success)
