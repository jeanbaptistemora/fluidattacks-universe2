from git.exc import (
    GitError,
)
from git.repo import (
    Repo,
)
from utils.logs import (
    log_blocking,
)

# Constants
DEFAULT_COMMIT: str = "0000000000000000000000000000000000000000"


def get_repo(path: str, search_parent_directories: bool = True) -> Repo:
    return Repo(path, search_parent_directories=search_parent_directories)


def get_repo_head_hash(path: str) -> str:
    try:
        repo: Repo = get_repo(path)
        head_hash: str = repo.head.commit.hexsha
        return head_hash
    except GitError as exc:
        log_blocking("error", "Computing commit hash: %s ", exc)

    return DEFAULT_COMMIT


def get_repo_branch(path: str) -> str | None:
    try:
        repo: Repo = get_repo(path)
        return repo.active_branch.name
    except GitError as exc:
        log_blocking("error", "Computing active branch: %s ", exc)
    except IndexError:
        return None

    return None


def get_repo_remote(path: str) -> str | None:
    url: str | None = None
    try:
        repo: Repo = get_repo(path)
        remotes = repo.remotes
        if remotes:
            url = remotes[0].url
            if url and not url.startswith("http"):
                url = f"ssh://{url}"
    except GitError as exc:
        log_blocking("error", "Computing active branch: %s ", exc)

    return url
