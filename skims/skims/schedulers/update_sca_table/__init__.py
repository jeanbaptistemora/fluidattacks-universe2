# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .repositories.advisories_community import (
    get_advisories_community,
    URL_ADVISORIES_COMMUNITY,
)
from .repositories.advisory_database import (
    get_advisory_database,
    URL_ADVISORY_DATABASE,
)
from db_model import (
    advisories as advisories_model,
)
from db_model.advisories.types import (
    Advisory,
)
from git import (
    GitError,
    Repo,
)
from s3.operations import (
    upload_advisories,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)

Advisories = List[Advisory]

REPOSITORIES: List[Tuple[Callable[[Advisories, str], None], str]] = [
    (
        get_advisories_community,
        URL_ADVISORIES_COMMUNITY,
    ),
    (
        get_advisory_database,
        URL_ADVISORY_DATABASE,
    ),
]


def fix_advisory(advisory: Advisory) -> Advisory:
    versions = advisory.vulnerable_version.split(" || ")
    if ">=0" in versions and len(versions) > 1:
        fixed_vers = [ver for ver in versions if ver != ">=0"]
        return advisory._replace(vulnerable_version=" || ".join(fixed_vers))
    return advisory


def clone_repo(url: str) -> Optional[str]:
    # pylint: disable=consider-using-with
    tmp_dirname = TemporaryDirectory().name
    try:
        print(f"cloning {url}")
        Repo.clone_from(url, tmp_dirname, depth=1)
    except GitError as error:
        log_blocking("error", f"Error cloning repository: {url}")
        print(error)
        return None
    return tmp_dirname


async def update_sca() -> None:
    # cloning repositories
    log_blocking("info", "Cloning neccesary repositories")
    tmp_repositories = [
        (fun, repo) for fun, url in REPOSITORIES if (repo := clone_repo(url))
    ]
    # processing vulnerable packages
    advisories: Advisories = []
    log_blocking("info", "Processing advisories")
    for get_ad, repo in tmp_repositories:
        get_ad(advisories, repo)

    # adding to table
    log_blocking("info", "Adding advisories to skima_sca table")
    to_storage: List[Advisory] = []
    for advisory in advisories:
        await advisories_model.add(
            advisory=fix_advisory(advisory), to_storage=to_storage
        )

    # adding to s3 bucket
    log_blocking("info", "Adding advisories to skima.sca bucket")
    await s3_start_resource()
    await upload_advisories(to_storage)
    await s3_shutdown()


async def main() -> None:
    await update_sca()
