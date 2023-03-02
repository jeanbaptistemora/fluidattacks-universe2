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
    schema: dict[str, Any] = {
        "additionalProperties": False,
        "patternProperties": {
            "^[a-z0-9_]+$": {
                "additionalProperties": False,
                "properties": {
                    "attempts": {"minimum": 1, "type": "integer"},
                    "awsRole": {"type": "string"},
                    "command": {
                        "items": {"type": "string"},
                        "minItems": 1,
                        "type": "array",
                    },
                    "enable": {"type": "boolean"},
                    "environment": {
                        "items": {"type": "string"},
                        "type": "array",
                    },
                    "meta": {
                        "additionalProperties": False,
                        "properties": {
                            "description": {"minLength": 0, "type": "string"},
                            "lastReview": {
                                "pattern": "^[0-9]{2}-[0-9]{2}-[0-9]{4}$",
                                "type": "string",
                            },
                            "maintainers": {
                                "items": {
                                    "pattern": "^[a-z]+$",
                                    "type": "string",
                                },
                                "minItems": 1,
                                "type": "array",
                            },
                            "requiredBy": {
                                "items": {"minLength": 10, "type": "string"},
                                "minItems": 0,
                                "type": "array",
                            },
                        },
                        "required": [
                            "description",
                            "lastReview",
                            "maintainers",
                            "requiredBy",
                        ],
                        "type": "object",
                    },
                    "parallel": {"minimum": 1, "type": "integer"},
                    "scheduleExpression": {"type": "string"},
                    "size": {"type": "string"},
                    "tags": {"type": "object"},
                    "timeout": {"minimum": 60, "type": "integer"},
                },
                "required": [
                    "attempts",
                    "awsRole",
                    "command",
                    "enable",
                    "environment",
                    "meta",
                    "parallel",
                    "scheduleExpression",
                    "size",
                    "tags",
                    "timeout",
                ],
                "type": "object",
            }
        },
        "propertyNames": {"pattern": "^[a-z0-9_]+$"},
        "type": "object",
    }
    validate(instance=data, schema=schema)


def test_meta_active_maintainers(*, data: dict[str, Any]) -> bool:
    success: bool = True
    repo: str = "fluidattacks/universe"
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
            variable_values={"fullPath": repo},
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
                " This means that none of the specified maintainers"
                f" has access to {repo}."
                " Schedules must have at least one active maintainer."
            )
            success = False

    return success


def test_meta_last_review(*, data: dict[str, Any]) -> bool:
    success: bool = True
    delta_months: int = 1
    time_format: str = "%d-%m-%Y"
    today: datetime = datetime.today()

    for name, values in data.items():
        last_review: datetime = datetime.strptime(
            values["meta"]["lastReview"],
            time_format,
        )
        next_review: datetime = last_review + relativedelta(
            months=delta_months
        )
        if today > next_review:
            success = False
            error(
                f"{name}.meta.lastReview was on"
                f" {last_review.strftime(time_format)}."
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
    success = success and test_meta_last_review(data=user_data)

    sys.exit(0 if success else 1)


main()
