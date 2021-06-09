# This migration attempts to fix errors caused due to:
#   https://gitlab.com/fluidattacks/product/-/issues/4765
#
# For all vulns on a finding,
# compute their hashes and find duplicates
#
# Execution time:
# Finalization time:

import boto3
from itertools import (
    groupby,
)
from typing import (
    Any,
    Dict,
    List,
)
from vulnerabilities.domain.utils import (
    get_hash_from_dict,
)

PROD: bool = False


def handle_finding_vulns(items: List[Dict[str, Any]]) -> None:
    finding_vulns: List[Dict[str, Any]] = [
        item
        for item in items
        if item.get("historic_state", [{}])[-1].get("state") == "open"
        and "masked" not in item.get("where", "").lower()
        and "masked" not in item.get("specific", "").lower()
    ]

    for _, _same_hash_vulns in groupby(finding_vulns, key=get_hash_from_dict):
        same_hash_vulns = tuple(_same_hash_vulns)
        if len(same_hash_vulns) >= 2:
            print("---")
            for vuln in same_hash_vulns:
                finding_id: str = vuln["finding_id"]
                uuid: str = vuln["UUID"]
                print(finding_id, uuid)


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
                handle_finding_vulns(finding_vulns)
                finding_id_last = finding_id
                finding_vulns = [item]

    resource = boto3.resource("dynamodb")
    table = resource.Table("FI_vulnerabilities")
    kwargs: Dict[str, Any] = dict(Limit=100)
    response = table.scan(**kwargs)
    handle_response(response)

    while "LastEvaluatedKey" in response:
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = table.scan(**kwargs)
        handle_response(response)


if __name__ == "__main__":
    main()
