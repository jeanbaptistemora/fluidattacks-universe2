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
    ],
)
async def test_get_toe_lines(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["data"]["group"]["roots"] == [
        {
            "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "toeLines": [
                {
                    "attackedAt": "2021-02-20T05:00:00+00:00",
                    "attackedBy": "test2@test.com",
                    "attackedLines": 4,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "comment 2",
                    "commitAuthor": "customer2@gmail.com",
                    "filename": "test2/test#.config",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "modifiedCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": 80,
                }
            ],
        },
        {
            "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "toeLines": [
                {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test@test.com",
                    "attackedLines": 23,
                    "bePresent": False,
                    "bePresentUntil": "2021-01-19T15:41:04+00:00",
                    "comments": "comment 1",
                    "commitAuthor": "customer1@gmail.com",
                    "filename": "test1/test.sh",
                    "firstAttackAt": "2020-01-19T15:41:04+00:00",
                    "loc": 4324,
                    "modifiedCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test3@test.com",
                    "attackedLines": 120,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "comment 3",
                    "commitAuthor": "customer3@gmail.com",
                    "filename": "test3/test.sh",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "modifiedCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
            ],
        },
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["reattacker@fluidattacks.com"],
        ["customer@gmail.com"],
        ["customer@fluidattacks.com"],
        ["customeradmin@gmail.com"],
        ["customeradmin@fluidattacks.com"],
        ["executive@gmail.com"],
        ["executive@fluidattacks.com"],
        ["system_owner@gmail.com"],
        ["system_owner@fluidattacks.com"],
        ["resourcer@gmail.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["reviewer@fluidattacks.com"],
        ["service_forces@gmail.com"],
        ["service_forces@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
