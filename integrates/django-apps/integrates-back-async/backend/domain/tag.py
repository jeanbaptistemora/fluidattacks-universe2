from contextlib import suppress
from typing import Dict, List, Optional, Union, cast

from aioextensions import collect

from backend.dal import tag as tag_dal
from backend.domain import (
    organization as org_domain,
    project as project_domain,
)
from backend.typing import Tag as TagType
from backend import authz


async def delete(organization: str, tag: str) -> bool:
    return await tag_dal.delete(organization, tag)


async def get_attributes(
    organization: str,
    tag: str,
    attributes: Optional[List[str]] = None
) -> Dict[str, Union[List[str], str]]:
    return await tag_dal.get_attributes(organization, tag, attributes)


async def get_tags(
        organization: str,
        attributes: Optional[List[str]] = None) -> List[TagType]:
    return await tag_dal.get_tags(organization, attributes)


async def is_tag_allowed(
        user_projects: List[Dict[str, Union[str, List[str]]]],
        organization: str,
        tag: str) -> bool:
    all_projects_tag = await get_attributes(organization, tag, ['projects'])
    user_projects_tag = [
        str(project.get('project_name', '')).lower()
        for project in user_projects
        if tag in [
            p_tag.lower()
            for p_tag in project.get('tag', [])
        ]
    ]
    return any(project.lower() in user_projects_tag
               for project in all_projects_tag.get('projects', []))


async def filter_allowed_tags(organization: str, user_projects: List[str]) -> \
        List[str]:
    projects = await collect(
        project_domain.get_attributes(
            project, ['tag', 'project_name']
        )
        for project in user_projects
    )
    all_tags = {
        str(tag.lower())
        for project in projects
        for tag in project.get('tag', [])
    }
    are_tags_allowed = await collect(
        is_tag_allowed(
            projects, organization, tag
        )
        for tag in all_tags
    )
    tags = [
        tag for tag, is_tag_allowed in zip(all_tags, are_tags_allowed)
        if is_tag_allowed
    ]
    return tags


async def has_user_access(email: str, subject: str) -> bool:
    with suppress(ValueError):
        org_id, portfolio = subject.split('PORTFOLIO#')
        org_name = await org_domain.get_name_by_id(org_id)
        portfolio_info = await get_attributes(
            org_name, portfolio, ['projects']
        )

        org_access, group_access = await collect((
            org_domain.has_user_access(
                email=email,
                organization_id=org_id
            ),
            authz.get_group_level_roles(
                email=email,
                groups=cast(List[str], portfolio_info.get('projects', []))
            )
        ))

        return org_access and any(group_access.values())

    raise ValueError('Invalid subject')
