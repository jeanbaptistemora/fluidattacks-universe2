#  pylint: disable=invalid-name
# This migration attempts to fix errors caused due to:
#   https://gitlab.com/fluidattacks/product/-/issues/4765
#
# For all vulns on a finding,
# compute their hashes and find duplicates
#
# Execution time: 2021-06-09T16:06:55+00:00
# Finalization time: 2021-06-09T16:41:42+00:00

import boto3
from datetime import (
    datetime,
)
from dateutil.parser import (  # type: ignore
    parse as parse_date,
)
from itertools import (
    groupby,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_hash_from_dict,
)

# Constants
PROD: bool = True

# Types
Item = Dict[str, Any]


def get_vuln_creation_date(vuln: Item) -> datetime:
    date_str: str = vuln.get("historic_state", [{}])[0].get("date", "")
    if date_str:
        return parse_date(date_str)
    raise KeyError("Unable to determine the creation date")


def split(vulns: List[Item]) -> Tuple[Item, List[Item]]:
    oldest = min(vulns, key=get_vuln_creation_date)
    remaining = [vuln for vuln in vulns if vuln["UUID"] != oldest["UUID"]]
    return oldest, remaining


def delete_vulns(vulns: List[Item], table: Any) -> None:
    for vuln in vulns:
        finding_id: str = vuln["finding_id"]
        uuid: str = vuln["UUID"]
        new_historic_entry = dict(
            analyst="kamado@fluidattacks.com",
            date="2021-06-09 11:00:00",
            justification="DUPLICATED",
            source="integrates",
            state="DELETED",
        )
        historic_state = vuln["historic_state"]
        historic_state.append(new_historic_entry)
        print(f"Updating {finding_id}, {uuid}: {historic_state}")

        if PROD:
            table.update_item(
                Key=dict(finding_id=finding_id, UUID=uuid),
                UpdateExpression="SET #historic_state = :historic_state",
                ExpressionAttributeNames={"#historic_state": "historic_state"},
                ExpressionAttributeValues={":historic_state": historic_state},
            )


def handle_finding_vulns(items: List[Item], table: Any) -> None:
    finding_vulns: List[Item] = [
        item
        for item in items
        if item.get("historic_state", [{}])[-1].get("state") == "open"
        and "masked" not in item.get("where", "").lower()
        and "masked" not in item.get("specific", "").lower()
    ]

    for _, _same_hash_vulns in groupby(finding_vulns, key=get_hash_from_dict):
        same_hash_vulns = list(_same_hash_vulns)
        if len(same_hash_vulns) >= 2:
            print("---")
            try:
                oldest, remaining = split(same_hash_vulns)
            except KeyError:
                print(f"An error ocurred: {same_hash_vulns}")
            else:
                print(f"Oldest: {oldest}")
                print(f"Remaining: {remaining}")
                delete_vulns(remaining, table)


def main() -> None:
    finding_id_last: str = ""
    finding_vulns: List[Dict[str, str]] = []

    def handle_response(response: Any) -> None:
        nonlocal finding_id_last, finding_vulns

        for item in response["Items"]:
            finding_id: str = item["finding_id"]

            if finding_id == finding_id_last:
                finding_vulns.append(item)
            else:
                handle_finding_vulns(finding_vulns, table)
                finding_id_last = finding_id
                finding_vulns = [item]

    resource = boto3.resource("dynamodb")
    table = resource.Table("FI_vulnerabilities")
    kwargs: Item = dict(Limit=100)
    response = table.scan(**kwargs)
    handle_response(response)

    while "LastEvaluatedKey" in response:
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = table.scan(**kwargs)
        handle_response(response)


if __name__ == "__main__":
    main()
