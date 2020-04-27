import sys
from typing import List
from asgiref.sync import sync_to_async
from backend.api.resolvers import project as project_loader
from backend.decorators import enforce_user_level_auth_async, require_login
from backend.domain import (
    project as project_domain, tag as tag_domain,
    user as user_domain
)
from backend.typing import Project as ProjectType, Tag as TagType
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


async def resolve(info, tag: str) -> TagType:
    """Async resolve fields."""
    result: TagType = dict()
    requested_fields = info.field_nodes[0].selection_set.selections
    user_email = util.get_jwt_content(info.context).get('user_email', '')
    projects: List[str] = await get_list_projects(user_email, tag)
    organization: str = '-'
    if projects:
        organizations = await sync_to_async(project_domain.get_attributes)(
            projects[0], ['companies'])
        organization = organizations.get('companies', ['-'])[0]

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
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


async def get_list_projects(user_email: str, tag: str) -> List[str]:
    projects = []
    user_projects = await sync_to_async(user_domain.get_projects)(user_email)
    for project in user_projects:
        project_attrs = await sync_to_async(project_domain.get_attributes)(
            project, ['tag'])
        project_tag = project_attrs.get('tag', [])
        project_tag = [proj_tag.lower() for proj_tag in project_tag]
        if tag in project_tag:
            projects.append(project.lower())
    return projects


async def _get_projects(info, projects: List[str], **__) -> List[ProjectType]:
    """Async resolve fields."""
    projects_list = [await project_loader.resolve(info, project, as_field=True)
                     for project in projects]
    return projects_list


async def _get_name(_, tag: str, **__) -> str:
    """Get tag name."""
    return tag


async def _get_last_closing_vuln(
        _, tag: str, organization: str, **__) -> float:
    """Get tag last_closing_vuln."""
    last_closing_vuln = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['last_closing_date']
        )
    last_closing_vuln = last_closing_vuln.get('last_closing_date', 0)
    return last_closing_vuln


async def _get_max_severity(_, tag: str, organization: str, **__) -> float:
    """Get tag max_severity."""
    max_severity = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['max_severity']
        )
    max_severity = max_severity.get('max_severity', 0)
    return max_severity


async def _get_max_open_severity(_, tag: str, organization: str,
                                 **__) -> float:
    """Resolve tag maximum severity"""
    max_open_severity = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['max_open_severity']
        )
    return max_open_severity.get('max_open_severity', 0)


async def _get_mean_remediate(_, tag: str, organization: str, **__) -> float:
    """Get tag mean_remediate."""
    mean_remediate = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['mean_remediate']
        )
    mean_remediate = mean_remediate.get('mean_remediate', 0)
    return mean_remediate


async def _get_mean_remediate_low_severity(
        _, tag: str, organization: str, **__) -> float:
    """Get tag mean_remediate_low_severity."""
    mean_remediate_low_severity = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['mean_remediate_low_severity']
        )
    mean_remediate_low_severity = mean_remediate_low_severity.get(
        'mean_remediate_low_severity', 0)
    return mean_remediate_low_severity


async def _get_mean_remediate_medium_severity(
        _, tag: str, organization: str, **__) -> float:
    """Get tag mean_remediate_medium_severity."""
    mean_remediate_medium_severity = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['mean_remediate_medium_severity']
        )
    mean_remediate_medium_severity = mean_remediate_medium_severity.get(
        'mean_remediate_medium_severity', 0)
    return mean_remediate_medium_severity


async def _get_mean_remediate_high_severity(
        _, tag: str, organization: str, **__) -> float:
    """Get tag mean_remediate_high_severity."""
    mean_remediate_high_severity = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['mean_remediate_high_severity']
        )
    mean_remediate_high_severity = mean_remediate_high_severity.get(
        'mean_remediate_high_severity', 0)
    return mean_remediate_high_severity


async def _get_mean_remediate_critical_severity(
        _, tag: str, organization: str, **__) -> float:
    """Get tag mean_remediate_critical_severity."""
    mean_critical_remediate = await \
        sync_to_async(tag_domain.get_attributes)(
            organization, tag, ['mean_remediate_critical_severity']
        )
    mean_critical_remediate = mean_critical_remediate.get(
        'mean_remediate_critical_severity', 0)
    return mean_critical_remediate


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
async def resolve_tag(_, info, tag: str) -> TagType:
    """Resolve alert query."""
    tag = tag.lower()
    return await resolve(info, tag)
