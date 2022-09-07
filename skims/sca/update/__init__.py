# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from git import (
    GitError,
    Repo,
)
import json
from repositories.advisories_community import (
    get_advisories_community,
    URL_ADVISORIES_COMMUNITY,
)
from repositories.advisory_database import (
    get_advisory_database,
    URL_ADVISORY_DATABASE,
)
import sys
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)

Advisories = Dict[str, Dict[str, str]]

ALL_PLATFORMS = "all"
REPOSITORIES: List[
    Tuple[Callable[[Advisories, str, str], dict], str, Iterable[str]]
] = [
    (
        get_advisories_community,
        URL_ADVISORIES_COMMUNITY,
        ("maven", "npm", "nuget", "pip"),
    ),
    (
        get_advisory_database,
        URL_ADVISORY_DATABASE,
        ("maven", "npm", "nuget", "pip"),
    ),
]
SUPPORTED_PLATFORMS = ("maven", "npm", "nuget", "pip")
VALID_ENTRIES = (ALL_PLATFORMS, *SUPPORTED_PLATFORMS)


def clone_repo(url: str) -> Optional[str]:
    tmp_dirname = TemporaryDirectory().name
    try:
        print(f"cloning {url}")
        Repo.clone_from(url, tmp_dirname, depth=1)
    except GitError as error:
        log_blocking("error", f"Error cloning repository: {url}")
        print(error)
        return None
    return tmp_dirname


def main() -> None:
    pltf = sys.argv[1] if len(sys.argv) > 1 else ""
    if pltf not in VALID_ENTRIES:
        log_blocking(
            "error",
            f"Invalid/Missing parameter. Valid entries: {' | '.join(VALID_ENTRIES)}",
        )
        return None

    # cloning repositories
    log_blocking("info", f"Cloning neccesary repositories")
    tmp_repositories = [
        (fun, repo, platforms)
        for fun, url, platforms in REPOSITORIES
        if pltf in (ALL_PLATFORMS, *platforms) and (repo := clone_repo(url))
    ]

    for platform in [pltf] if pltf != ALL_PLATFORMS else SUPPORTED_PLATFORMS:
        advisories: Advisories = {}
        log_blocking("info", f"Processing vulnerabilities for {platform}")
        for get_ad, repo, platforms in tmp_repositories:
            if platform in platforms:
                get_ad(advisories, repo, platform)
        log_blocking("info", f"Creating file: {platform}.json")
        with open(f"static/sca/{platform}.json", "w") as outfile:
            json.dump(advisories, outfile, indent=2, sort_keys=True)
            outfile.write("\n")


main()
