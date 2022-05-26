#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
This migration is needed to add the protocol field to some repositories that
do not have it, probably due to an incomplete migration when the field was
implemented.
Mssing this field causes some actions like activating/deactivating a repository
to end in failure

Execution Time:     2020-05-19 19:35 UTC-5
Finalization Time:  2020-05-13 19:37 UTC-5
"""
import argparse
import bugsnag
from custom_types import (
    Group as GroupType,
    Resource as ResourceType,
)
from groups.dal import (  # pylint: disable=import-error
    get_all as get_all_groups,
    TABLE_NAME as GROUP_TABLE,
)
import hashlib
import json
from typing import (
    cast,
    Dict,
    List,
    Tuple,
)
from urllib.parse import (
    ParseResult,
    urlparse,
)


def get_default_protocol(group: GroupType) -> str:
    """
    If the protocol cannot be extracted from the URL, use the most common
    protocol across the group's resources
    """
    protocol_count: Dict[str, int] = {"HTTPS": 0, "SSH": 0}
    for repo in cast(List[ResourceType], group["repositories"]):
        protocol: str = cast(str, repo.get("protocol", ""))
        if protocol:
            protocol_count[protocol] += 1
    protocols: List[str] = list(protocol_count.keys())
    count: List[int] = list(protocol_count.values())
    return protocols[count.index(max(count))]


def get_repositories_hash(repositories: List[ResourceType]) -> str:
    return hashlib.sha512(json.dumps(repositories).encode()).hexdigest()


def has_repos_without_protocol(project: GroupType) -> bool:
    result: bool = False
    for repo in cast(List[ResourceType], project.get("repositories", [])):
        if not repo.get("protocol", ""):
            result = True
            break
    return result


def process_repos(
    group: GroupType, default_protocol: str, execute: bool
) -> Tuple[List[ResourceType], str]:
    allowed_protocols: List[str] = ["SSH", "HTTPS"]
    repos: List[ResourceType] = cast(List[ResourceType], group["repositories"])

    field_hash: str = ""
    if not execute:
        field_hash = get_repositories_hash(repos)

    for repo in repos:
        if not repo.get("protocol", ""):
            repo_url: ParseResult = urlparse(cast(str, repo["urlRepo"]))
            protocol: str = default_protocol
            if (
                repo_url.scheme
                and repo_url.scheme.upper() in allowed_protocols
            ):
                protocol = repo_url.scheme.upper()
            repo.update({"protocol": protocol})

    return repos, field_hash


def add_protocol_to_repos(
    group: GroupType, default_protocol: str, execute: bool, dry_run: bool
) -> None:
    group_name: str = cast(str, group["project_name"])
    if execute:
        old_field_hash: str = cast(str, group["repositories-hash"])
        current_field_hash: str = get_repositories_hash(
            cast(List[ResourceType], group["repositories"])
        )
        processed_repos: List[ResourceType] = cast(
            List[ResourceType], group["repositories-new"]
        )
        if old_field_hash != current_field_hash:
            processed_repos, _ = process_repos(
                group, default_protocol, execute
            )
        response = GROUP_TABLE.update_item(
            Key={"project_name": group_name},
            UpdateExpression=(
                "SET #attr1Name = :val1 REMOVE #attr2Name, #attr3Name"
            ),
            ExpressionAttributeNames={
                "#attr1Name": "repositories",
                "#attr2Name": "repositories-new",
                "#attr3Name": "repositories-hash",
            },
            ExpressionAttributeValues={":val1": processed_repos},
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            log(
                (
                    "Migration 0002: Repositories successfully migrated for "
                    f"group {group_name}"
                ),
                dry_run,
            )
    else:
        repos, field_hash = process_repos(group, default_protocol, execute)
        if dry_run:
            print(
                f"Repositories from group {group_name} will be changed "
                "as follows:"
            )
            for repo in repos:
                print("----")
                for key, value in repo.items():
                    print(f"    {key}: {value}")
            print(f"    {field_hash}")
        else:
            response = GROUP_TABLE.update_item(
                Key={"project_name": group_name},
                UpdateExpression="SET #attr1Name = :val1, #attr2Name = :val2",
                ExpressionAttributeNames={
                    "#attr1Name": "repositories-new",
                    "#attr2Name": "repositories-hash",
                },
                ExpressionAttributeValues={
                    ":val1": repos,
                    ":val2": field_hash,
                },
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                log(
                    (
                        "Migration 0002: Protocol successfully added "
                        f"to repos of project {group_name}"
                    ),
                    dry_run,
                )


def log(message: str, dry_run: bool) -> None:
    if not dry_run:
        bugsnag.notify(Exception(message), severity="info")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", required=False, action="store_true")
    ap.add_argument("--execute", required=False, action="store_true")

    args: Dict[str, bool] = vars(ap.parse_args())
    dry_run_flag: bool = args["dry_run"]
    execute_flag: bool = args["execute"]

    log(
        "Starting migration 0002 to ensure all repositories "
        "have protocol field",
        dry_run_flag,
    )

    for group_to_process in get_all_groups():
        if has_repos_without_protocol(group_to_process):
            default_protocol_to_use: str = get_default_protocol(
                group_to_process
            )
            log(
                (
                    f"Migration 0002: processing group "
                    f'{group_to_process["project_name"]} with default '
                    f"protocol {default_protocol_to_use}"
                ),
                dry_run_flag,
            )
            add_protocol_to_repos(
                group_to_process,
                default_protocol_to_use,
                execute_flag,
                dry_run_flag,
            )
