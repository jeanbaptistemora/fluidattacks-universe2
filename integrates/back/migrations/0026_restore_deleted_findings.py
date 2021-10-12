# pylint: disable=invalid-name,import-error
# Formerly a draft was identified by 'not having a releaseDate' in the DB.
# This was migrated and a new column called 'historic_state' was added.
# When this was done there was a missing migration, and now you can find
# Findings with historic state like this:
#
# finding_id = 123456
# release_date = 2019-06-26 00:00:00
# historic_state =
# [{'analyst': 'xxxxx@fluidattacks.com',
#   'date': '2020-04-17 12:39:26',
#   'state': 'CREATED'},
#  {'analyst': 'xxxxx@fluidattacks.com',
#   'date': '2020-08-12 09:12:16',
#   'justification': 'NOT_REQUIRED',
#   'state': 'DELETED'}]
#
# And with 'releaseDate', this means a finding that the customer can see
# But that was deleted by confusing it with a Draft (was never submitted nor
# approved)
#
# Discovered around: 2020-06-25 13:00:00+00:00
# Fixed in DB around: 2020-08-26 20:32:36+00:00
#
# Damage: 5 findings were hidden from the customer in 3 different groups
#   during a timespan of 1 day to 2 weeks
#


import aioboto3
from aioextensions import (
    collect,
)
from asyncio import (
    run,
)
from dynamodb.operations_legacy import (
    RESOURCE_OPTIONS,
)
from findings.dal import (
    update,
)
import os
from pprint import (
    pprint,
)
from typing import (
    Any,
)

STAGE: str = os.environ["STAGE"]
FINDINGS_TABLE = "FI_findings"


async def scan(*, table_name: str, **options: Any) -> Any:
    async with aioboto3.resource(RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(table_name)
        response = await table.scan(**options)
        for elem in response.get("Items", []):
            yield elem

        while "LastEvaluatedKey" in response:
            options["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await table.scan(**options)
            for elem in response.get("Items", []):
                yield elem


async def main() -> None:
    updates = []
    async for finding in scan(table_name=FINDINGS_TABLE):
        if (
            # We don't care about wiped findings
            finding.get("finding") == "WIPED"
            or finding.get("affected_systems") == "Masked"
        ):
            continue

        finding_id = finding["finding_id"]
        old_historic_state = finding.get("historic_state", [])
        historic_state = old_historic_state.copy()

        # If has release date it was approved and the customer saw it
        #
        # If was deleted before being approved in the historic state
        # It means that someone deleted the finding by confusing it with a
        # draft due to the missing APPROVED state
        release_date = finding.get("releaseDate")
        if (
            release_date
            and len(historic_state) >= 2
            and historic_state[-1]["state"] == "DELETED"
            and historic_state[-2] != {}
            and historic_state[-2]["state"] != "APPROVED"
        ):
            # Remove the last state (the deleted one)
            historic_state.pop()

            print("=" * 80)
            print(f"finding_id = {finding_id}")
            print(f'project_name = {finding["project_name"]}')
            print(f"release_date = {release_date}")
            print("old_historic_state =")
            pprint(old_historic_state)
            print("historic_state =")
            pprint(historic_state)

            updates.append(
                update(finding_id, {"historic_state": historic_state})
            )

    print(f"Success: {all(await collect(updates, workers=64))}")


if __name__ == "__main__":
    run(main())
