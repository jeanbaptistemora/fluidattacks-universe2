# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
This migration encodes all environments and repositories using urllib
in all groups

Execution Time:     2020-06-30 18:39 UTC-5
Finalization Time:  2020-06-30 18:40 UTC-5

"""

import bugsnag
from groups import (
    dal as groups_dal,
)
import os
from urllib.parse import (
    quote,
    unquote,
)

STAGE: str = os.environ["STAGE"]


def log(message: str) -> None:
    print(message)
    if STAGE != "test":
        bugsnag.notify(Exception(message), severity="info")


def main() -> None:  # noqa: MC0001
    """
    Update resources
    """
    log("Starting migration 0015")
    all_groups = groups_dal.get_all(
        filtering_exp=(
            "attribute_exists(environments) or attribute_exists(repositories)"
        ),
        data_attr="project_name,environments,repositories",
    )

    if STAGE == "test":
        log("Resources will be updated as follows:")

    for group in all_groups:
        group_name = group.get("project_name")

        if STAGE == "test":
            log(f"---\nGroup: {group_name}")

        repos = group.get("repositories", [])
        for repo in repos:
            url = repo.get("urlRepo", "")
            url_enc = quote(url)
            branch = repo.get("branch", "")
            branch_enc = quote(branch)
            # Update only no encoded repositories
            if url != quote(unquote(url)):
                if STAGE == "test":
                    log(f"---\nrepo before: {repo}")
                repo["urlRepo"] = url_enc
                if STAGE == "test":
                    log(f"---\nrepo after: {repo}")
            elif branch != quote(unquote(branch)):
                if STAGE == "test":
                    log(f"---\nrepo before: {repo}")
                repo["branch"] = branch_enc
                if STAGE == "test":
                    log(f"---\nrepo after: {repo}")

            else:
                if STAGE == "test":
                    log(f"---\nrepo is already encoded: {repo}")

        envs = group.get("environments", [])
        for env in envs:
            url = env.get("urlEnv", "")

            url_enc = quote(url)
            # Update only no encoded environments
            if url != quote(unquote(url)):
                if STAGE == "test":
                    log(f"---\nenv before: {env}")

                env["urlEnv"] = url_enc

                if STAGE == "test":
                    log(f"---\nenv after: {env}")
            else:
                if STAGE == "test":
                    log(f"---\nenv is already encoded: {env}")

        if STAGE != "test":
            success: bool = groups_dal.update(
                group_name, {"environments": envs, "repositories": repos}
            )
            if success:
                log(f"Migration 0015: Group {group_name} succesfully encoded")


if __name__ == "__main__":
    main()
