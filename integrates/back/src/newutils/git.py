from context import (
    SERVICES_GITLAB_API_TOKEN,
    SERVICES_GITLAB_API_USER,
)
from git import (
    Repo,
)


def clone_services_repository(path: str) -> None:
    """Clone the services repository into a local directory"""
    repo_url = (
        f"https://{SERVICES_GITLAB_API_USER}:{SERVICES_GITLAB_API_TOKEN}"
        "@gitlab.com/fluidattacks/services.git"
    )
    Repo.clone_from(
        repo_url,
        path,
        multi_options=[
            "--depth=1",
        ],
    )


def get_last_file_hash(repo: Repo, filename: str) -> str:
    """Get last hash of a file in the repo"""
    return repo.git.log("--max-count", "1", "--format=%H", "--", filename)


def get_last_file_date(repo: Repo, filename: str) -> str:
    """Get last modified date of a file in the repo"""
    return repo.git.log("--max-count", "1", "--format=%cI", "--", filename)
