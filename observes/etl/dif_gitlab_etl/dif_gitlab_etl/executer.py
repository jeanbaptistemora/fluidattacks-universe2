"""
Binds functions of other modules to specific parameters.
Supports the interface used by cli.
"""
# Standard libraries
from typing import (
    Any, Callable,
    Dict,
    List,
    Optional,
)
# Third party libraries
# Local libraries
from dif_gitlab_etl import db_client
from dif_gitlab_etl import etl
from dif_gitlab_etl import planner
from dif_gitlab_etl.db_client import DbState
from dif_gitlab_etl.etl import ExtractState
from dif_gitlab_etl.utils import log

from streamer_gitlab import page_data
from streamer_gitlab.api_client import (
    GitlabResource,
    GResourcePageRange,
)
from streamer_gitlab.log import MaxRetriesReached
from streamer_gitlab.page_data import PageData


def specific_resources(project: str) -> List[GitlabResource]:
    return [
        GitlabResource(
            project=project,
            resource='jobs',
        ),
        GitlabResource(
            project=project,
            resource='merge_requests',
            params=frozenset({'scope': 'all'}.items())
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


def statement_executer_function(
    db_state: DbState
) -> Callable[[str], None]:
    def statement_exe(statement: str) -> None:
        db_client.execute(db_state, statement)
    return statement_exe


def exe_and_fetch_function(
    db_state: DbState
) -> Callable[[str], List[Any]]:
    def exe_and_fetch(statement: str) -> List[Any]:
        executer = statement_executer_function(db_state)
        executer(statement)
        return db_state.cursor.fetchall()
    return exe_and_fetch


def start_etl(project: str, auth: Dict[str, str]):
    log('info', f'Starting Gitlab ETL for {project}')
    db_state = db_client.make_access_point(auth)
    stm_executer = exe_and_fetch_function(db_state)
    resources: List[GitlabResource] = specific_resources(project)
    for resource in resources:
        try:
            interval: range = planner.get_work_interval(
                resource, stm_executer, 250
            )
            lgu_id: int = planner.get_lgu_id(resource, stm_executer)
            data_pages: PageData = etl.extract_pages_data(
                resource_range=GResourcePageRange(
                    g_resource=resource,
                    page_range=interval,
                    per_page=100,
                ),
                last_greatest_uploaded_id=lgu_id,
                extract_range=extract_range_function()
            )
            etl.upload_data(
                list(reversed(data_pages)), auth,
                statement_executer_function(db_state)
            )
        except MaxRetriesReached:
            continue


async def start_etls(projects: List[str], auth: Dict[str, str]):
    for project in projects:
        start_etl(project, auth)
