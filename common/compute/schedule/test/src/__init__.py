from datetime import (
    datetime,
)
from dateutil.relativedelta import (
    relativedelta,
)
from gql import (
    Client,
    gql,
)
from gql.transport.aiohttp import (
    AIOHTTPTransport,
)
from graphql import (
    DocumentNode,
)
import json
from jsonschema import (
    validate,
)
import os
import sys
from typing import (
    Any,
)


def error(msg: str) -> None:
    print("[ERROR]", msg)


def test_data_schema(*, data: dict[str, Any]) -> None:
    schema: dict[str, Any] = json.loads(os.environ["SCHEMA"])
    validate(instance=data, schema=schema)


def test_meta_active_maintainers(*, data: dict[str, Any]) -> bool:
    success: bool = True
    session: Client = Client(
        transport=AIOHTTPTransport(
            url="https://gitlab.com/api/graphql",
            headers={
                "Authorization": f"Bearer {os.environ['UNIVERSE_API_TOKEN']}"
            },
        ),
        fetch_schema_from_transport=True,
    )
    query: DocumentNode = gql(
        """
        query getProjectUsers ($fullPath: ID!) {
            project(fullPath: $fullPath) {
                projectMembers {
                    edges {
                        node {
                            user {
                                username
                            }
                        }
                    }
                }
            }
        }
        """
    )
    result: dict[str, Any] = dict(
        session.execute(
            query,
            variable_values={"fullPath": "fluidattacks/universe"},
        )
    )
    users: list[str] = [
        edge["node"]["user"]["username"].removesuffix("atfluid")
        for edge in result["project"]["projectMembers"]["edges"]
    ]

    for name, values in data.items():
        if not any(user in users for user in values["meta"]["maintainers"]):
            error(
                f"No active users found in '{name}.meta.maintainers'."
                " Schedules must have at least one active maintainer."
            )
            success = False

    return success


def test_meta_last_reviewed(*, data: dict[str, Any]) -> bool:
    success: bool = True
    delta_months: int = 1
    time_format: str = "%d-%m-%Y"
    today: datetime = datetime.today()

    for name, values in data.items():
        last_reviewed: datetime = datetime.strptime(
            values["meta"]["lastReviewed"],
            time_format,
        )
        next_review: datetime = last_reviewed + relativedelta(
            months=delta_months
        )
        if today > next_review:
            success = False
            error(
                f"{name}.meta.lastReviewed was on"
                f" {last_reviewed.strftime(time_format)}."
                " Please review and update the schedule."
            )

    return success


def main() -> None:
    success: bool = True

    data: dict[str, Any] = json.loads(os.environ["DATA"])
    test_data_schema(data=data)

    success = success and test_meta_active_maintainers(data=data)

    user_data: dict[str, Any] = {
        name: values
        for (name, values) in data.items()
        if os.environ["CI_COMMIT_REF_NAME"].removesuffix("atfluid")
        in values["meta"]["maintainers"]
    }
    success = success and test_meta_last_reviewed(data=user_data)

    sys.exit(0 if success else 1)


main()
