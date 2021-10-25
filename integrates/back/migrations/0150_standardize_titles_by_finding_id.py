# pylint: disable=invalid-name
"""
This migration aims to standardize all findings titles, found in:
https://gitlab.com/fluidattacks/product/-/blob/master/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml

Similar to migration 0109, but using the new db model

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
    FindingMetadataToUpdate,
)
from db_model.findings.update import (
    update_metadata,
)
import time

PROD: bool = False


async def _process_finding(
    loaders: Dataloaders,
    finding_id: str,
    new_title: str,
) -> str:
    try:
        finding: Finding = await loaders.finding.load(finding_id)
    except FindingNotFound:
        print(f"   --- Deleted: {finding_id}")
        return f"DELETED status for {finding_id}"

    if PROD:
        await update_metadata(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=FindingMetadataToUpdate(title=new_title),
        )
        print(f"   === Updated: {finding.group_name} - {finding.id}")
        return f"Renaming done for {finding_id}"

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
    loaders: Dataloaders = get_new_context()
    results = await collect(
        (
            _process_finding(
                loaders=loaders,
                finding_id=finding["finding_id"],
                new_title=finding["title"],
            )
            for finding in new_data
        ),
        workers=4,
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
