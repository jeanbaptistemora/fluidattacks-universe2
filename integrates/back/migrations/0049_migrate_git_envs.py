# /usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration dumps envs from services yml to the new roots table

Execution Time: 2020-12-18 16:32:02 UTC-5
Finalization Time: 2020-12-18 16:32:23 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from groups import (
    domain as groups_domain,
)
import os
import re
from roots import (
    domain as roots_domain,
)
from typing import (
    List,
    NamedTuple,
    Optional,
    Tuple,
)
from urllib.parse import (
    unquote,
)
import yaml  # type: ignore

STAGE: str = os.environ["STAGE"]
SERVICES_REPO_DIR: str = f"{os.getcwd()}/services"

Application = NamedTuple(
    "Application",
    [
        ("url", Optional[List[str]]),
    ],
)

GroupConfig = NamedTuple(
    "GroupConfig",
    [
        ("application", Optional[Application]),
    ],
)


def get_group_config(group_name: str) -> GroupConfig:
    config_path: str = os.path.join(
        SERVICES_REPO_DIR, "groups", group_name, "config", "config.yml"
    )

    with open(config_path, mode="r", encoding="utf8") as config_file:
        config = yaml.safe_load(config_file)

        return GroupConfig(
            application=(
                Application(url=config["application"].get("url"))
                if "application" in config
                else None
            ),
        )


def get_envs_by_group(group_name: str) -> List[str]:
    config: GroupConfig = get_group_config(group_name)
    envs: List[str] = (
        config.application.url
        if config.application and config.application.url
        else []
    )

    return envs


def format_old_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.strptime(date, "%Y-%m-%d %H:%M")


async def get_oldest_active_repo(group_name: str) -> Tuple[str, str]:
    old_repos = (
        await groups_domain.get_attributes(group_name, ["repositories"])
    ).get("repositories", [])
    active_repos = [
        (
            format_old_date(
                repo["historic_state"][-1]["date"].replace("/", "-")
            ),
            repo["urlRepo"],
            repo["branch"],
        )
        for repo in old_repos
        if repo.get("historic_state", [{}])[-1].get("state") == "ACTIVE"
    ]
    if active_repos:
        _, url, branch = min(active_repos)
        return (url, branch)

    print(f"[WARNING] {group_name} has no active repos, won't migrate")
    return ("", "")


def format_old_url(url: str) -> str:
    """Transforms the url in an effort to increase the matches"""
    unquoted: str = unquote(unquote(url)).rstrip("/")
    without_git: str = unquoted.replace(".git", "").replace("_git/", "")
    # Discard protocols as most old urls don't have it
    without_protocol: str = re.sub(r"(ssh|http(s)?):\/\/", "", without_git)
    # Get the last two paths
    path: str = "/".join(without_protocol.split("/")[1:][-2:])
    # Some old urls have no path, they're not even urls, just the repo name
    formatted: str = path if path else without_protocol

    return formatted.strip().lower()


async def update_envs(group_name: str) -> None:
    context = get_new_context()
    url, branch = await get_oldest_active_repo(group_name)

    if url and branch:
        roots = await roots_domain.get_roots_by_group(group_name)
        matching_root = next(
            (
                root
                for root in roots
                if format_old_url(url) in root["url"].strip().lower()
                and branch.strip().lower() == root["branch"].strip().lower()
            ),
            None,
        )

        if matching_root:
            print(
                f"[INFO] Match in {group_name}",
                "\nOLD:",
                (url, branch),
                "\nNEW:",
                (matching_root["url"], matching_root["branch"]),
            )

            if matching_root["historic_state"][-1]["state"] == "ACTIVE":
                if STAGE != "test":
                    envs: List[str] = get_envs_by_group(group_name)
                    await roots_domain.update_git_environments(
                        loaders=context,
                        user_email="",
                        group_name=group_name,
                        root_id=matching_root["sk"],
                        environment_urls=envs,
                    )
            else:
                print(
                    "[WARNING]",
                    group_name,
                    matching_root["sk"],
                    "inactive, won't migrate",
                )
        else:
            print("[INFO] No match found", group_name, url, branch)


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, "groups"))
    print(f"[INFO] Found {len(groups)} groups")

    await collect(update_envs(group_name) for group_name in groups)


if __name__ == "__main__":
    run(main())
