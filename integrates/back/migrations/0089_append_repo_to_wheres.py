#  pylint: disable=invalid-name
# This migration attempts to fix errors caused due to:
#   https://gitlab.com/fluidattacks/product/-/issues/4714
#
# For all lines vulns with repo_nickname,
# we'll append the repo_nickname to the where
# so it follows the repo/path/to/file format
#
# Execution time: 2021-06-01 18:40:18-05:00
# Finalization time: 2021-06-01 20:44:12-05:00

import boto3
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
        repo: Optional[str] = item.get("repo_nickname")

        if (
            repo
            and type_ == "lines"
            and where
            and "masked" not in where.lower()
            and not where.startswith(repo)
        ):
            correct_where: str = f"{repo}/{where}"

            print()
            print(f"  finding_id:    {finding_id}")
            print(f"  uuid:          {uuid}")
            print(f"  where:         {where}")
            print(f"  correct_where: {correct_where}")

            if PROD:
                table.update_item(
                    Key=dict(finding_id=finding_id, UUID=uuid),
                    UpdateExpression="SET #where = :where",
                    ExpressionAttributeNames={"#where": "where"},
                    ExpressionAttributeValues={":where": correct_where},
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
