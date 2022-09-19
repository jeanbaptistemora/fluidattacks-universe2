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
from custom_exceptions import (
    UnavailabilityError,
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
    upload_object,
)
from s3.resource import (
    get_s3_resource,
    s3_shutdown,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Any,
    Callable,
    Dict,
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


async def upload_to_s3(to_storage: List[Advisory]) -> None:
    s3_advisories: Dict[str, Any] = {}
    for adv in to_storage:
        if adv.package_manager not in s3_advisories:
            s3_advisories.update({adv.package_manager: {}})
        if adv.package_name not in s3_advisories[adv.package_manager]:
            s3_advisories[adv.package_manager].update({adv.package_name: {}})
        s3_advisories[adv.package_manager][adv.package_name].update(
            {adv.associated_advisory: adv.vulnerable_version}
        )
    try:
        client = await get_s3_resource()
        for key, value in s3_advisories.items():
            print(key)
            await upload_object(
                client=client,
                bucket="skims.sca",
                dict_object=value,
                file_name=f"{key}.json",
            )
    except UnavailabilityError as ex:
        log_blocking("error", "%s", ex.new())
    finally:
        await s3_shutdown()


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
    await upload_to_s3(to_storage)


async def main() -> None:
    await update_sca()
