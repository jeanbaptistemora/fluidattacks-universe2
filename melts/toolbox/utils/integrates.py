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
    regexps = tuple(rule for root in filters for rule in root['paths']
                    if root['policy'] == 'INCLUDE')
    return regexps or ('^.*$', )


def get_exclude_rules(group: str) -> Tuple[str, ...]:
    filter_request = api.integrates.Queries.git_roots_filter(API_TOKEN, group)
    if not filter_request.ok:
        logger.error(filter_request.errors)
        return tuple()
    filters = tuple(rule['filter']
                    for rule in filter_request.data['project']['roots'])
    return tuple(rule for root in filters for rule in root['paths']
                 if root['policy'] == 'EXCLUDE')
