# pylint: disable=import-error

from asgiref.sync import sync_to_async
from backend.api.resolvers import project as project_loader
from backend.decorators import enforce_user_level_auth_async, require_login
from backend.domain import (
    project as project_domain,
    user as user_domain
)
from backend import util

from ariadne import convert_kwargs_to_snake_case


async def _resolve_fields(info, tag: str):
    """Async resolve fields."""
    jwt_content = util.get_jwt_content(info.context)
    user_email = jwt_content.get('user_email')
    user_projects = await sync_to_async(user_domain.get_projects)(user_email)
    projects = []
    for project in user_projects:
        project_attrs = await sync_to_async(project_domain.get_attributes)(
            project, ['tag'])
        project_tag = project_attrs.get('tag', [])
        project_tag = [proj_tag.lower() for proj_tag in project_tag]
        if tag in project_tag:
            projects.append(project.lower())
    projects_list = [await project_loader.resolve(info, project, as_field=True)
                     for project in projects]
    return {
        'name': tag,
        'projects': projects_list
    }


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
def resolve_tag(_, info, tag: str):
    """Resolve alert query."""
    tag = tag.lower()
    return util.run_async(_resolve_fields, info, tag)
