from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_ports")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["customer_manager@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
    ],
)
async def test_get_toe_ports(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["data"]["group"]["toePorts"] == {
        "edges": [
            {
                "cursor": (
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk9"
                    "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAj"
                    "QUREUkVTUyMxOTIuMTY4LjEuMSNQT1JUIzgwODAifQ=="
                ),
                "node": {
                    "address": "192.168.1.1",
                    "attackedAt": "2020-01-02T05:00:00+00:00",
                    "attackedBy": "admin@gmail.com",
                    "bePresent": True,
                    "bePresentUntil": None,
                    "firstAttackAt": "2020-01-02T05:00:00+00:00",
                    "hasVulnerabilities": True,
                    "port": 8080,
                    "root": {
                        "__typename": "IPRoot",
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "root1",
                    },
                    "seenAt": "2000-01-01T05:00:00+00:00",
                    "seenFirstTimeBy": "test1@test.com",
                },
            },
            {
                "cursor": (
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk"
                    "9PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjQU"
                    "REUkVTUyMxOTIuMTY4LjEuMSNQT1JUIzgwODEifQ=="
                ),
                "node": {
                    "address": "192.168.1.1",
                    "attackedAt": "2021-02-11T05:00:00+00:00",
                    "attackedBy": "admin@gmail.com",
                    "bePresent": False,
                    "bePresentUntil": "2021-03-11T05:00:00+00:00",
                    "firstAttackAt": "2021-02-11T05:00:00+00:00",
                    "hasVulnerabilities": False,
                    "port": 8081,
                    "root": {
                        "__typename": "IPRoot",
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "root2",
                    },
                    "seenAt": "2020-01-11T05:00:00+00:00",
                    "seenFirstTimeBy": "test2@test.com",
                },
            },
        ],
        "pageInfo": {
            "endCursor": (
                "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjQU"
                "REUkVTUyMxOTIuMTY4LjEuMSNQT1JUIzgwODEifQ=="
            ),
            "hasNextPage": False,
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_ports")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["architect@fluidattacks.com"],
        ["architect@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@fluidattacks.com"],
        ["user@gmail.com"],
        ["user_manager@fluidattacks.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@fluidattacks.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@fluidattacks.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_get_toe_ports_error(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
