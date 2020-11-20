# pylint: disable=method-hidden

from typing import Dict, List, Union, cast

from aiodataloader import DataLoader
from aioextensions import collect
from backend.domain import project as project_domain
from backend.typing import Project as ProjectType


async def _batch_load_fn(
        projects: List[str]) -> List[Dict[str, Union[List[str], ProjectType]]]:
    """Batch the data load requests within the same execution fragment."""
    projects_data: Dict[str, Union[List[str], ProjectType]] = dict()

    finding_coroutines = project_domain.list_findings(projects)
    draft_coroutines = project_domain.list_drafts(projects)
    group_coroutines = project_domain.get_many_groups(projects)
    list_groups, list_findings, list_drafts = await collect([
        group_coroutines, finding_coroutines, draft_coroutines
    ])

    for group_name, group_info, findings, drafts in zip(
        projects, list_groups, list_findings, list_drafts
    ):
        projects_data[group_name] = dict(
            findings=findings,
            drafts=drafts,
            attrs=group_info
        )

    return [
        cast(
            Dict[str, Union[List[str], ProjectType]],
            projects_data.get(project, dict())
        )
        for project in projects
    ]


# pylint: disable=too-few-public-methods
class ProjectLoader(DataLoader):  # type: ignore
    async def batch_load_fn(
        self,
        projects: List[str]
    ) -> List[Dict[str, Union[List[str], ProjectType]]]:
        return await _batch_load_fn(projects)
