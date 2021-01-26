# Standard library
import json
import multiprocessing.pool
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

# Third import
from retry import retry

# Local imports
from toolbox import api
from toolbox.constants import API_TOKEN
from toolbox import logger
from toolbox.api.exceptions import IntegratesError


def get_project_repos(project: str) -> List:
    """Return the repositories for a project."""
    repositories: List[str] = []
    response = api.integrates.Queries.resources(
        api_token=API_TOKEN,
        project_name=project)
    if response.ok:
        repositories = json.loads(response.data['resources']['repositories'])
    else:
        logger.error(f'An error has occurred querying the {project} group')
        logger.error(response.errors)

    return repositories


def get_filter_rules(group: str) -> List[Dict[str, Any]]:
    filter_request = api.integrates.Queries.git_roots_filter(API_TOKEN, group)
    if not filter_request.ok:
        logger.error(f'An error has occurred querying the {group} group')
        logger.error(filter_request.errors)
        return list()
    return filter_request.data['project']['roots']


@retry(IntegratesError, tries=10, delay=5, logger=logger)  # type: ignore
def has_forces(group: str) -> bool:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        logger.error(f'An error has occurred querying the {group} group')
        raise IntegratesError(response.errors)

    return response.data['project']['hasForces']


@retry(IntegratesError, tries=10, delay=5, logger=logger)  # type: ignore
def get_group_language(group: str) -> str:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        logger.error(f'An error has occurred querying the {group} group')
        raise IntegratesError(response.errors)

    return response.data['project']['language']


@retry(IntegratesError, tries=10, delay=5, logger=logger)  # type: ignore
def has_drills(group: str) -> bool:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        logger.error(f'An error has occurred querying the {group} group')
        raise IntegratesError(response.errors)

    return response.data['project']['hasDrills']


def filter_groups_with_forces(groups: Tuple[str, ...]) -> Tuple[str, ...]:
    with multiprocessing.pool.ThreadPool(10) as pool:
        return tuple(
            group
            for group, group_has_forces in zip(
                groups, pool.map(has_forces, groups),
            )
            if group_has_forces
        )


def filter_groups_with_forces_as_json_str(groups: Tuple[str, ...]) -> bool:
    print(json.dumps(filter_groups_with_forces(groups)))
    return True


def update_root_cloning_status(
    root_id: str,
    status: str,
    message: str,
) -> bool:
    result = api.integrates.Mutations.update_cloning_status(
        API_TOKEN,
        root_id,
        status,
        message,
    )
    if status not in {'OK', 'FAILED', 'UNKNOWN'}:
        raise ValueError(f'{status} is an ivalid status')

    if result.errors:
        logger.error('An error has occurred updating the status: {0}'.format(
            result.errors[0]['message']))
        return False
    if not result.data['updateRootCloningStatus']['success']:
        logger.error('An error has occurred updating the status')
    return result.data['updateRootCloningStatus']['success']
