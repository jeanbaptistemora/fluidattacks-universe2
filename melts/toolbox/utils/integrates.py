# Standard library
import json
from typing import (
    List,
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
