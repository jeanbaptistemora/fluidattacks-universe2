# pylint: disable=invalid-name
"""
This migration adds a RANDOM_AVAILABLE_GROUP_SORT attribute
and an uuid to the integrates table on the available group items
so it is possible to get a group name randomly querying by a gsi

1st execution
Execution Time: 2020-06-04 12:30 UTC-5
Finalization Time: 2020-06-04 12:42 UTC-5

2nd execution
First was interrupted because a token expiration
Function was modified to migrate only the left items
Execution Time: 2020-06-04 13:31 UTC-5
Finalization Time: 2020-06-04 13:35 UTC-5
"""

from boto3.dynamodb.conditions import (
    Key,
)
import bugsnag
from names.dal import (
    TABLE_NAME as INTEGRATES_TABLE,
)
import os
from typing import (
    List,
)
import uuid

STAGE: str = os.environ["STAGE"]


def log(message: str) -> None:
    print(message)
    bugsnag.notify(Exception(message), severity="info")


def get_availabe_without_uuid() -> List[str]:
    key_exp = Key("pk").eq("AVAILABLE_GROUP")
    response = INTEGRATES_TABLE.query(
        KeyConditionExpression=key_exp,
        FilterExpression="attribute_not_exists(#gsi2pk)",
        ExpressionAttributeNames={"#gsi2pk": "gsi-2-pk"},
        ProjectionExpression="sk",
    )
    all_available = response["Items"]
    while response.get("LastEvaluatedKey"):
        response = INTEGRATES_TABLE.query(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            KeyConditionExpression=key_exp,
            FilterExpression="attribute_not_exists(#gsi2pk)",
            ExpressionAttributeNames={"#gsi2pk": "gsi-2-pk"},
            ProjectionExpression="sk",
        )
        all_available += response["Items"]
    return [available["sk"] for available in all_available]


def main() -> None:
    """
    Get all available group names and assign an uuid
    """
    log("Starting migration 0008")
    all_available = get_availabe_without_uuid()

    if STAGE == "test":
        log("Available groups will be added as follows:")

    for avail_group in all_available:

        if STAGE == "test":
            log(
                "pk: AVAILABLE_GROUP\n"
                f"sk: {avail_group}\n"
                "gsi-2-pk: RANDOM_AVAILABLE_GROUP_SORT\n"
                "gsi-2-sk: new_uuid4"
            )

        else:
            response = INTEGRATES_TABLE.update_item(
                Key={"pk": "AVAILABLE_GROUP", "sk": avail_group},
                UpdateExpression="SET #gsi2pk = :val1, #gsi2sk = :val2",
                ConditionExpression="attribute_not_exists(#gsi2pk)",
                ExpressionAttributeNames={
                    "#gsi2pk": "gsi-2-pk",
                    "#gsi2sk": "gsi-2-sk",
                },
                ExpressionAttributeValues={
                    ":val1": "RANDOM_AVAILABLE_GROUP_SORT",
                    ":val2": str(uuid.uuid4()),
                },
                ReturnValues="ALL_NEW",
            )
            log(response)


if __name__ == "__main__":
    main()
