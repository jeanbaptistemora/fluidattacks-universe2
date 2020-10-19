"""
Binds functions of other modules to specific parameters.
Supports the interface used by cli.
"""
# Standard libraries
from typing import (
    Callable, List,
    Optional,
)
# Third party libraries
# Local libraries
from dif_gitlab_etl import etl
from dif_gitlab_etl import page_data
from dif_gitlab_etl import planner
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GResourcePageRange,
)
from dif_gitlab_etl.etl import ExtractState


def specific_resources(project: str) -> List[GitlabResource]:
    return [
        GitlabResource(
            project=project,
            resource='jobs',
        ),
        GitlabResource(
            project=project,
            resource='merge_requests',
        )
    ]


def extract_range_function() -> Callable[
    [GResourcePageRange, Optional[int]], ExtractState
]:
    def extract_range(
        resource_range: GResourcePageRange,
        init_last_minor_id: Optional[int] = None
    ) -> ExtractState:
        return etl.extract_between(
            resource_range=resource_range,
            extract_data=page_data.extract_data,
            extract_data_less_than=page_data.extract_data_less_than,
            init_last_minor_id=init_last_minor_id,
        )
    return extract_range


def start_etl(project):
    resources: List[GitlabResource] = specific_resources(project)
    for resource in resources:
        interval: range = planner.get_work_interval(resource)
        lgu_id: int = planner.get_lgu_id(resource)
        extract_status: ExtractState = etl.extract_pages_data(
            resource_range=GResourcePageRange(
                g_resource=resource,
                page_range=interval,
                per_page=100,
            ),
            last_greatest_uploaded_id=lgu_id,
            extract_range=extract_range_function()
        )
        etl.upload_data(extract_status.data_pages)
