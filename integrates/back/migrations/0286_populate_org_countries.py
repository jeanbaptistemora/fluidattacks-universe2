# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
"""
Sets the country attribute for current orgs

Execution Time:    2022-09-22 at 15:08:24 UTC
Finalization Time: 2022-09-22 at 15:08:36 UTC
"""

from aioextensions import (
    run,
)
import csv
from db_model import (
    TABLE,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
import logging.config
from organizations.domain import (
    iterate_organizations,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)

CSV_PATH = "/path/to/countries_arm.csv"


async def main() -> None:
    org_countries: dict[str, str] = {}
    with open(CSV_PATH, "r", encoding="utf-8") as source:
        data = csv.reader(source)
        next(data)
        for row in data:
            if row[1]:
                org_countries[row[0]] = row[1]

    async for organization in iterate_organizations():
        if organization.name in org_countries:
            await operations.update_item(
                item={"country": org_countries[organization.name]},
                key=PrimaryKey(
                    partition_key=organization.id,
                    sort_key=f"ORG#{organization.name}",
                ),
                table=TABLE,
            )
        else:
            LOGGER.info("%s not found", organization.name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
