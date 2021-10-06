# /usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration dumps group repos to the new roots table

Execution Time: 2020-12-04 10:59:58 UTC-5
Finalization Time: 2020-12-04 11:01:55 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
import os
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)
from urllib.parse import (
    unquote,
)
import yaml  # type: ignore

STAGE: str = os.environ["STAGE"]
SERVICES_REPO_DIR: str = f"{os.getcwd()}/services"

Code = NamedTuple("Code", [("branches", List[str]), ("url", List[str])])

Filter = NamedTuple("Filter", [("authorized_by", str), ("regex", str)])

Lines = NamedTuple(
    "Lines", [("exclude", List[Filter]), ("include", List[Filter])]
)

Coverage = NamedTuple("Coverage", [("lines", Lines)])

GroupConfig = NamedTuple(
    "GroupConfig", [("code", List[Code]), ("coverage", Coverage)]
)


def get_group_config(group_name: str) -> GroupConfig:
    config_path: str = os.path.join(
        SERVICES_REPO_DIR, "groups", group_name, "config", "config.yml"
    )
    with open(config_path, mode="r", encoding="utf8") as config_file:
        config = yaml.safe_load(config_file)
        code = config.get("code", [])
        coverage = config["coverage"]

        return GroupConfig(
            code=[
                Code(branches=code["branches"], url=code["url"])
                for code in code
            ],
            coverage=Coverage(
                lines=Lines(
                    exclude=[
                        Filter(**exclusion)
                        for exclusion in coverage["lines"]["exclude"]
                    ],
                    include=[
                        Filter(**inclusion)
                        for inclusion in coverage["lines"]["include"]
                    ],
                )
            ),
        )


def get_filter_config(lines: Lines) -> Dict[str, Any]:
    has_include: bool = lines.include[0].regex != "^.*$"
    policy: str = "INCLUDE" if has_include else "EXCLUDE"

    return {
        "paths": [filter_.regex for filter_ in getattr(lines, policy.lower())],
        "policy": policy,
    }


def get_roots_by_group(group_name: str) -> List[Dict[str, Any]]:
    print(f"[Info] Working on {group_name}")
    config: GroupConfig = get_group_config(group_name)
    filter_config = get_filter_config(config.coverage.lines)

    return [
        {
            "branch": branch,
            "environment": "",
            "filter": filter_config,
            "group_name": group_name,
            "includes_health_check": False,
            "url": unquote(code_config.url[0]),
        }
        for code_config in config.code
        for branch in code_config.branches
    ]


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, "groups"))
    print(f"[INFO] Found {len(groups)} groups")
    roots = [
        root
        for group_name in groups
        for root in get_roots_by_group(group_name)
    ]

    if STAGE == "test":
        print(f"Will migrate a total of {len(roots)} roots")
        for root in roots:
            print(root["group_name"], root["url"], root["branch"])
    else:
        await collect(roots_domain.add_git_root("", **root) for root in roots)


if __name__ == "__main__":
    run(main())
