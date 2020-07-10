# pylint: disable=method-hidden

import asyncio
from typing import Dict, List
from asgiref.sync import sync_to_async
from aiodataloader import DataLoader
from backend.domain import project as project_domain


async def _batch_load_fn(projects: List[str]):
    """Batch the data load requests within the same execution fragment."""
    projects_data: Dict = dict()
    list_findings_tasks = [
        asyncio.create_task(
            sync_to_async(project_domain.list_findings)(project.lower())
        )
        for project in projects
    ]
    list_drafts_tasks = [
        asyncio.create_task(
            sync_to_async(project_domain.list_drafts)(project.lower())
        )
        for project in projects
    ]
    get_attributes_tasks = [
        asyncio.create_task(
            sync_to_async(project_domain.get_attributes)(project.lower(), [])
        )
        for project in projects
    ]
    findings = await asyncio.gather(*list_findings_tasks)
    drafts = await asyncio.gather(*list_drafts_tasks)
    attrs = await asyncio.gather(*get_attributes_tasks)

    for project in projects:
        projects_data[project] = dict(
            findings=findings.pop(0),
            drafts=drafts.pop(0),
            attrs=attrs.pop(0)
        )

    return [projects_data.get(project, dict()) for project in projects]


# pylint: disable=too-few-public-methods
class ProjectLoader(DataLoader):
    async def batch_load_fn(self, projects: List[str]):
        return await _batch_load_fn(projects)
