# pylint: disable=invalid-name
"""
This migration aims to standardize all findings titles, found in:
https://gitlab.com/fluidattacks/product/-/blob/master/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml

Similar to migration 0109, but using the new db model

Execution Time:     2021-10-25 at 22:43:36 UTC
Finalization Time:  2021-10-25 at 22:45:41 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
import csv
from custom_exceptions import (
    FindingNotFound,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    FindingMetadataToUpdate,
)
from db_model.findings.update import (
    update_metadata,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
import time

PROD: bool = True


async def _get_group(finding_id: str) -> str:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        table=TABLE,
    )
    if not results:
        raise FindingNotFound()
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=results,
    )

    return metadata["group_name"]


async def _process_finding(
    finding_id: str,
    new_title: str,
) -> str:
    try:
        group_name: str = await _get_group(finding_id=finding_id)
        print(group_name)
    except FindingNotFound:
        print(f"   --- Deleted: {finding_id}")
        return f"DELETED status for {finding_id}"

    if PROD:
        await update_metadata(
            group_name=group_name,
            finding_id=finding_id,
            metadata=FindingMetadataToUpdate(title=new_title),
        )
        print(f"   === Updated: {group_name} - {finding_id}")
        return f"Renaming OK for {finding_id}"

    return f"No processed yet {finding_id}"


async def main() -> None:
    # Read new titles info
    with open("0150.csv", mode="r", encoding="utf8") as in_file:
        reader = csv.reader(in_file)
        new_data = [
            {
                "finding_id": rows[0],
                "title": rows[1],
            }
            for rows in reader
            if rows[0] != "finding_id"  # Skip header
        ]

    print(f"   === findings to update: {len(new_data)}")
    print(f"   === sample: {new_data[:3]}")

    # Retrieve and process
    results = await collect(
        _process_finding(
            finding_id=finding["finding_id"],
            new_title=finding["title"],
        )
        for finding in new_data
    )

    # Store results locally
    with open("0150_results.txt", mode="a", encoding="utf8") as out_file:
        for result in results:
            out_file.write(f"{result}\n")

    print("   === done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
