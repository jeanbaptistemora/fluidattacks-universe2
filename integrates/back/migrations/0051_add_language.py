# /usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration adds the language field to the project based on the config.yml

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from groups import (
    dal as groups_dal,
)
import os
from typing import (
    Dict,
    List,
)
import yaml  # type: ignore

# Constants
SERVICES_REPO_DIR: str = f"{os.getcwd()}/services"


async def update_project(group_name: str, language: str) -> None:
    await groups_dal.update(group_name, {"language": language})


def get_language(group_name: str) -> str:
    print(f"[INFO] Working on {group_name}")
    config_path: str = os.path.join(
        SERVICES_REPO_DIR,
        "groups",
        group_name,
        "config",
        "config.yml",
    )
    with open(config_path, mode="r", encoding="utf8") as config_file:
        config: Dict[str, str] = yaml.safe_load(config_file)
        return config["language"]


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, "groups"))
    print(f"[INFO] Found {len(groups)} groups")

    await collect(
        update_project(group_name, get_language(group_name))
        for group_name in groups
    )


if __name__ == "__main__":
    run(main())
