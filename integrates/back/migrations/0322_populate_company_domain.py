# pylint: disable=import-error,invalid-name
# type: ignore
"""
Populates gsi2 with the domain name of the company,
which will be used to validate trial uniqueness per company

Execution Time:    2022-12-05 at 19:37:59 UTC
Finalization Time: 2022-12-05 at 19:38:00 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from datetime import (
    datetime,
)
from db_model import (
    companies as companies_model,
)
from db_model.companies.types import (
    Company,
    Trial,
)
import time


async def process_trial(row: dict[str, str]) -> None:
    await companies_model.add(
        company=Company(
            domain=row["domain"],
            trial=Trial(
                completed=row["completed"] == str(True),
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(row["start_date"]),
            ),
        )
    )


async def main() -> None:
    with open("/path/to/trial.csv", "r", encoding="utf8") as trial_csv:
        reader = csv.DictReader(trial_csv, delimiter=",")
        await collect([process_trial(row) for row in reader])


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
