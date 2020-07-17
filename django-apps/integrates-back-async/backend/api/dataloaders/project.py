# pylint: disable=method-hidden

import asyncio
from typing import Dict, List
from aiodataloader import DataLoader
from backend.domain import project as project_domain


async def _batch_load_fn(projects: List[str]):
    """Batch the data load requests within the same execution fragment."""
    projects_data: Dict = dict()

    finding_task = asyncio.create_task(project_domain.list_findings(projects))
    draft_task = asyncio.create_task(project_domain.list_drafts(projects))
    group_task = asyncio.create_task(project_domain.get_many_groups(projects))
    list_groups, list_findings, list_drafts = await asyncio.gather(
        group_task, finding_task, draft_task
    )

    for group_name, group_info, findings, drafts in zip(
        projects, list_groups, list_findings, list_drafts
    ):
        projects_data[group_name] = dict(
            findings=findings,
            drafts=drafts,
            attrs=group_info
        )

    return [projects_data.get(project, dict()) for project in projects]


# pylint: disable=too-few-public-methods
class ProjectLoader(DataLoader):
    async def batch_load_fn(self, projects: List[str]):
        return await _batch_load_fn(projects)
