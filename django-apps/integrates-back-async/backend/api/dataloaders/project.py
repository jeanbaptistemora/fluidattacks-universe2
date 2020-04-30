# pylint: disable=method-hidden

from typing import Dict, List
from asgiref.sync import sync_to_async
from backend.domain import project as project_domain
from aiodataloader import DataLoader


async def _batch_load_fn(projects: List[str]):
    """Batch the data load requests within the same execution fragment."""
    projects_data: Dict = dict()

    for project in projects:
        findings = await sync_to_async(project_domain.list_findings)(project)
        drafts = await sync_to_async(project_domain.list_drafts)(project)
        attrs = await sync_to_async(project_domain.get_attributes)(project, [])
        projects_data[project] = dict(
            findings=findings,
            drafts=drafts,
            attrs=attrs
        )

    return [projects_data.get(project, dict()) for project in projects]


# pylint: disable=too-few-public-methods
class ProjectLoader(DataLoader):
    async def batch_load_fn(self, projects: List[str]):
        return await _batch_load_fn(projects)
