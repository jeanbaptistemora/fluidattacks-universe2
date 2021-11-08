from aioextensions import (
    in_thread,
)
from context import (
    SERVICES_GITLAB_API_TOKEN,
    SERVICES_GITLAB_API_USER,
)
from datetime import (
    datetime,
)
from git import (
    Repo,
)
from newutils import (
    datetime as datetime_utils,
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


async def get_last_commit_hash(repo: Repo, filename: str) -> str:
    """Get last hash of a file in the repo"""
    return str(
        await in_thread(
            repo.git.log, "--max-count", "1", "--format=%H", "--", filename
        )
    )


async def get_last_modified_date(repo: Repo, filename: str) -> str:
    """Get last modified date of a file in the repo"""
    return datetime_utils.get_as_utc_iso_format(
        datetime.fromisoformat(
            await in_thread(
                repo.git.log,
                "--max-count",
                "1",
                "--format=%cI",
                "--",
                filename,
            )
        )
    )
