# Standard library
import json
from typing import (
    List,
    Tuple,
)

# Local imports
from toolbox import api
from toolbox.constants import API_TOKEN
from toolbox import logger


def get_project_repos(project: str) -> List:
    """Return the repositories for a project."""
    repositories: List[str] = []
    response = api.integrates.Queries.resources(
        api_token=API_TOKEN,
        project_name=project)
    if response.ok:
        repositories = json.loads(response.data['resources']['repositories'])
    else:
        logger.error(response.errors)

    return repositories


def get_include_rules(group: str) -> Tuple[str, ...]:
    filter_request = api.integrates.Queries.git_roots_filter(API_TOKEN, group)
    if not filter_request.ok:
        logger.error(filter_request.errors)
        return tuple()
    filters = tuple(rule['filter']
                    for rule in filter_request.data['project']['roots'])
    return tuple(rule for root in filters for rule in root['include'])


def get_exclude_rules(group: str) -> Tuple[str, ...]:
    filter_request = api.integrates.Queries.git_roots_filter(API_TOKEN, group)
    if not filter_request.ok:
        logger.error(filter_request.errors)
        return tuple()
    filters = tuple(rule['filter']
                    for rule in filter_request.data['project']['roots'])
    return tuple(rule for root in filters for rule in root['exclude'])


def has_forces(group: str) -> bool:
    response = api.integrates.Queries.has_forces(API_TOKEN, group)
    success = False
    if response.ok:
        success = response.data['project']['hasForces']
    else:
        logger.error(response.errors[0])
    return success


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
