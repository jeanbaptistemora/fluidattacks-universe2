# pylint: disable=invalid-name
"""
This migration is used to delete duplicate entries in the 'repositories' field
of several groups introduced on 2020-05-12

Execution Time:     2020-05-13 17:13 UTC-5
Finalization Time:  2020-05-13 17:14 UTC-5
"""

import bugsnag
from custom_types import (
    Historic as HistoricType,
    Resource as ResourceType,
)
from groups.dal import (
    get_all as get_all_groups,
    TABLE_NAME as GROUP_TABLE,
)
from typing import (
    cast,
    List,
)


def get_unique_repos(repos: List[ResourceType]) -> List[ResourceType]:
    unique_repos_names = []
    unique_repos: List[ResourceType] = []
    for repo in repos:
        if repo["urlRepo"] not in unique_repos_names:
            unique_repos_names.append(repo["urlRepo"])
            unique_repos.append(repo)
        else:
            existing_repo_index = unique_repos_names.index(repo["urlRepo"])
            existing_repo = unique_repos[existing_repo_index]
            existing_repo_historic: HistoricType = existing_repo[
                "historic_state"
            ]
            repo_historic: HistoricType = repo["historic_state"]
            if repo_historic[-1]["date"] > existing_repo_historic[-1]["date"]:
                unique_repos[existing_repo_index] = repo
    return unique_repos


def remove_duplicated_repos() -> None:
    groups = get_all_groups()
    for group in groups:
        group_name: str = group["project_name"]
        try:
            if has_repeated_repos(group_name, []):  # type: ignore # pylint: disable=undefined-variable # noqa: F821
                bugsnag.notify(
                    Exception(
                        f"Migration 0001: Processing group {group_name}..."
                    ),
                    severity="info",
                )
                repos: List[ResourceType] = get_unique_repos(
                    cast(List[ResourceType], group["repositories"])
                )
                response = GROUP_TABLE.update_item(
                    Key={"project_name": group_name},
                    UpdateExpression="SET #attrName = :val1",
                    ExpressionAttributeNames={"#attrName": "repositories"},
                    ExpressionAttributeValues={":val1": repos},
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    bugsnag.notify(
                        Exception(
                            "Migration 0001: Duplicate repositories "
                            f"successfully erased from group {group_name}"
                        ),
                        severity="info",
                    )
                else:
                    bugsnag.notify(
                        Exception(
                            "Migration 0001: There was an error erasing "
                            f"duplicates from group {group_name}"
                        ),
                        severity="info",
                    )
        except KeyError:
            bugsnag.notify(
                Exception(
                    f"Migration 0001: Group {group_name} errored "
                    "during analysis of duplicates"
                ),
                severity="info",
            )


if __name__ == "__main__":
    bugsnag.notify(
        Exception("Starting migration 0001 to delete duplicated repositories"),
        severity="info",
    )
    remove_duplicated_repos()
