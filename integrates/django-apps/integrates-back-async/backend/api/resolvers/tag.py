import sys
from typing import List, Any

from ariadne import (
    convert_kwargs_to_snake_case,
    convert_camel_case_to_snake
)
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    require_login
)
from backend.domain import (
    organization as org_domain,
    tag as tag_domain,
    user as user_domain
)
from backend.typing import (
    Tag as TagType
)
from backend import util


async def resolve(info: GraphQLResolveInfo, tag: str) -> TagType:
    """Async resolve fields."""
    result: TagType = dict()
    requested_fields = info.field_nodes[0].selection_set.selections
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info.get('user_email', '')
    projects: List[str] = await get_list_projects(info, user_email, tag)
    organization: str = '-'
    if projects:
        project_attrs = await info.context.loaders['project'].load(projects[0])
        project_attrs = project_attrs['attrs']
        org_id = await org_domain.get_id_for_group(
            project_attrs['project_name']
        )
        organization = await org_domain.get_name_by_id(org_id)
    allowed_tags = await tag_domain.filter_allowed_tags(
        organization, projects)
    if tag not in allowed_tags:
        raise GraphQLError('Access denied')
    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'tag': tag,
            'organization': organization,
            'projects': projects,
            'requested_fields': requested_fields
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


async def get_list_projects(
        info: GraphQLResolveInfo,
        user_email: str,
        tag: str) -> List[str]:
    projects = []
    user_projects = await user_domain.get_projects(
        user_email,
        access_pending_projects=False
    )
    for project in user_projects:
        project_attrs = await info.context.loaders['project'].load(project)
        project_attrs = project_attrs['attrs']
        project_tag = project_attrs.get('tag', [])
        project_tag = [proj_tag.lower() for proj_tag in project_tag]
        if (tag in project_tag and
                project_attrs.get('project_status') == 'ACTIVE'):
            projects.append(project.lower())
    return projects


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_tag(_: Any, info: GraphQLResolveInfo, tag: str) -> TagType:
    """Resolve alert query."""
    tag = tag.lower()
    return await resolve(info, tag)
