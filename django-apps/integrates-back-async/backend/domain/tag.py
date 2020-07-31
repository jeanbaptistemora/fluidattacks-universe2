import asyncio
from typing import Dict, List, Optional, Union

from asgiref.sync import sync_to_async

from backend.dal import tag as tag_dal
from backend.domain import project as project_domain
from backend.typing import Tag as TagType


async def delete(organization: str, tag: str) -> bool:
    return await tag_dal.delete(organization, tag)


def get_attributes(organization: str, tag: str,
                   attributes: List[str]) -> Dict[str, Union[List[str], str]]:
    return tag_dal.get_attributes(organization, tag, attributes)


async def get_tags(
        organization: str,
        attributes: Optional[List[str]] = None) -> List[TagType]:
    return await tag_dal.get_tags(organization, attributes)


def is_tag_allowed(user_projects: List[Dict[str, Union[str, List[str]]]],
                   organization: str, tag: str) -> bool:
    all_projects_tag = get_attributes(organization, tag, ['projects'])
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
    projects = await asyncio.gather(*[
        project_domain.get_attributes(
            project, ['tag', 'project_name']
        )
        for project in user_projects
    ])
    all_tags = {
        tag.lower()
        for project in projects
        for tag in project.get('tag', [])
    }
    are_tags_allowed = await asyncio.gather(*[
        sync_to_async(is_tag_allowed)(
            projects, organization, tag
        )
        for tag in all_tags
    ])
    tags = [
        tag for tag in all_tags
        if are_tags_allowed.pop(0)
    ]
    return tags
