# Third party libraries
from git import Repo

# Local libraries
from __init__ import (
    SERVICES_GITLAB_API_TOKEN,
    SERVICES_GITLAB_API_USER,
)


def clone_services_repository(path: str) -> None:
    """Clone the services repository into a local directory"""
    repo_url = (
        f'https://{SERVICES_GITLAB_API_USER}:{SERVICES_GITLAB_API_TOKEN}'
        '@gitlab.com/fluidattacks/services.git'
    )
    Repo.clone_from(repo_url, path, branch='master')
