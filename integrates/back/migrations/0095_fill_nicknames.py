# pylint: disable=invalid-name
# This migration attempts fill the repo_nickname field
# of vulnerabilities of type lines:
#   https://gitlab.com/fluidattacks/product/-/issues/4840
#
# For all lines vulns without repo_nickname,
# we'll guess the repo_nickname from the where
# from the template repo_nickname/path/to/file
#
# Execution time: 2021-06-25T17:42:10+00:00
# Finalization time: 2021-06-29T15:31:55+00:00

import boto3
import os
from typing import (
    Any,
    Dict,
    Optional,
)

PROD: bool = True


def handle_response(table: Any, response: Any) -> None:
    for item in response["Items"]:
        finding_id: str = item["finding_id"]
        uuid: str = item["UUID"]
        where: Optional[str] = item.get("where")
        type_: str = item["vuln_type"]
        repo_nickname: Optional[str] = item.get("repo_nickname")

        if (
            not repo_nickname
            and type_ == "lines"
            and where
            and "masked" not in where.lower()
        ):
            repo_nickname = os.path.basename(where[::-1])[::-1]
            if not repo_nickname:
                # can happen when where is /an/absolute/path
                continue

            print()
            print(f"  finding_id:    {finding_id}")
            print(f"  uuid:          {uuid}")
            print(f"  where:         {where}")
            print(f"  repo_nickname: {repo_nickname}")

            if PROD:
                table.update_item(
                    Key=dict(finding_id=finding_id, UUID=uuid),
                    UpdateExpression="SET #repo_nickname = :repo_nickname",
                    ExpressionAttributeNames={
                        "#repo_nickname": "repo_nickname"
                    },
                    ExpressionAttributeValues={
                        ":repo_nickname": repo_nickname
                    },
                )


def main() -> None:
    resource = boto3.resource("dynamodb")
    table = resource.Table("FI_vulnerabilities")
    kwargs: Dict[str, str] = {}
    response = table.scan(**kwargs)
    handle_response(table, response)

    while "LastEvaluatedKey" in response:
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = table.scan(**kwargs)
        handle_response(table, response)


if __name__ == "__main__":
    main()
