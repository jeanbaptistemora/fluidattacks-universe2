from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["customer_manager@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
    ],
)
async def test_get_toe_lines(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-02-20T05:00:00+00:00",
                    "attackedBy": "test2@test.com",
                    "attackedLines": 4,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 2",
                    "lastAuthor": "customer2@gmail.com",
                    "filename": "test2/test#.config",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "lastCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": 80,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OT"
                "AjRklMRU5BTUUjdGVzdDIvdGVzdCMuY29uZmlnIn0=",
            },
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test@test.com",
                    "attackedLines": 23,
                    "bePresent": False,
                    "bePresentUntil": "2021-01-19T15:41:04+00:00",
                    "comments": "comment 1",
                    "lastAuthor": "customer1@gmail.com",
                    "filename": "test1/test.sh",
                    "firstAttackAt": "2020-01-19T15:41:04+00:00",
                    "loc": 4324,
                    "lastCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "asm_1",
                    },
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
                "EjRklMRU5BTUUjdGVzdDEvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test3@test.com",
                    "attackedLines": 120,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 3",
                    "lastAuthor": "customer3@gmail.com",
                    "filename": "test3/test.sh",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "lastCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "asm_1",
                    },
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
                "EjRklMRU5BTUUjdGVzdDMvdGVzdC5zaCJ9",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
            "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
            "EjRklMRU5BTUUjdGVzdDMvdGVzdC5zaCJ9",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["architect@fluidattacks.com"],
        ["architect@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["user@fluidattacks.com"],
        ["user@gmail.com"],
        ["user_manager@fluidattacks.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@fluidattacks.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@fluidattacks.com"],
        ["executive@gmail.com"],
        ["customer_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@fluidattacks.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_get_toe_lines_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
