# type: ignore

# pylint: disable=import-error,invalid-name
"""
Clear flag enrolled in enrollment_metadata facet for stakeholders
previously removed due to inactivity.

Execution Time:    2023-02-03 at 14:54:28 UTC
Finalization Time: 2023-02-03 at 14:56:43 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    get_new_context,
)
from db_model import (
    enrollment as enrollment_model,
)
from db_model.enrollment.types import (
    EnrollmentMetadataToUpdate,
)
import time


async def process_email(email: str) -> None:
    loaders = get_new_context()
    enrollment = await loaders.enrollment.load(email)
    if enrollment.enrolled is False:
        return

    orgs_access = await loaders.stakeholder_organizations_access.load(email)
    if len(orgs_access) > 0:
        return

    groups_access = await loaders.stakeholder_groups_access.load(email)
    if len(groups_access) > 0:
        return

    await enrollment_model.update_metadata(
        email=email,
        metadata=EnrollmentMetadataToUpdate(enrolled=False),
    )
    print(f"Updated {email=}")


async def main() -> None:
    with open("0358_data.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        emails = sorted([rows[0] for rows in reader])
        print(f"{len(emails)=}")

        await collect(
            tuple(process_email(email) for email in emails),
            workers=8,
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
