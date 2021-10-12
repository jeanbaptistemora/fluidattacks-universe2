# pylint: disable=invalid-name,import-error
# Formerly a draft was identified by 'not having a releaseDate' in the DB.
# This was migrated and a new column called 'historic_state' was added.
# When this was done there was a missing migration, and now you can find
# Findings with historic state like this:
#
#   "historic_state": [
#     {
#       "date": "2019-10-16 16:50:02",
#       "state": "SUBMITTED"
#     },
#     {
#       "analyst": "xxxxxxxxxx@fluidattacks.com",
#       "date": "2019-10-17 17:37:13",
#       "state": "REJECTED"
#     }
#   ]
#
# And with 'releaseDate', this means a finding that the customer can see
# But which for practical purposes is still a Draft (was never submitted nor
# approved)
#
#
# Discovered around: 2019-11-27
# Fixed in DB around: 2020-08-26 18:43:31+00:00
#


import aioboto3
from aioextensions import (
    collect,
)
from asyncio import (
    run,
)
import dateutil.parser  # type: ignore
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
            # If the finding has releaseDate it means it is visible to the
            # customer. We are interested in fixing those
            or "releaseDate" not in finding
        ):
            continue

        finding_id = finding["finding_id"]
        release_date = finding["releaseDate"]
        old_historic_state = finding.get("historic_state", [])
        historic_state = finding.get("historic_state", [])

        # It must have been created at some point in time by someone so fix it
        if (
            # historic_state is mandatory
            not historic_state
            # first state must be CREATED
            or historic_state[0].get("state") != "CREATED"
        ):
            item = {
                "analyst": finding["analyst"],
                # Use the report date if present or the releaseDate if not
                "date": finding.get("report_date") or finding["releaseDate"],
                "state": "CREATED",
            }
            # I do not know why this useless default value exists
            if historic_state == [{}]:
                # Fix it
                historic_state = [item]
            else:
                # Append the created item at the beggining
                historic_state.insert(0, item)

        # If it has a releaseDate then its last item must be
        #  APPROVED or DELETED
        #
        if release_date:
            if historic_state[-1]["state"] == "DELETED":
                # If it was DELETED then we consider it's ok
                pass
            elif historic_state[-1]["state"] == "APPROVED":
                # If it is APPROVED then we consider it's ok
                pass
            else:
                # The last state must be APPROVED
                historic_state.append(
                    {
                        "analyst": finding["analyst"],
                        "date": finding["releaseDate"],
                        "state": "APPROVED",
                    }
                )

                # If there is a time travel let's adjust it
                # the releaseDate only stores the day and not the hour
                # so if a finding was created and released the same day
                # there will be a difference due to the missing hour data
                # making it look like a time travel
                if dateutil.parser.parse(
                    historic_state[-1]["date"]
                ) < dateutil.parser.parse(historic_state[-2]["date"]):
                    historic_state[-1]["date"] = historic_state[-2]["date"]

                print("=" * 80)
                print(f"finding_id = {finding_id}")
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
