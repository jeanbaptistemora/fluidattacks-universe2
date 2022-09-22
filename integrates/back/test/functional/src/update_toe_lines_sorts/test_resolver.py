# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
    query_get,
)
from custom_exceptions import (
    InvalidSortsRiskLevel,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(("sorts_risk_level"), ((0), (10), (100)))
@pytest.mark.parametrize(
    ("sorts_suggestions"),
    (
        (
            [
                {
                    "findingTitle": "014. Insecure functionality",
                    "probability": 55,
                },
                {
                    "findingTitle": "007. Cross-site request forgery",
                    "probability": 44,
                },
                {
                    "findingTitle": "083. XML injection (XXE)",
                    "probability": 0,
                },
            ]
        ),
    ),
)
async def test_update_toe_lines_sorts(
    populate: bool,
    sorts_risk_level: int,
    sorts_suggestions: list[dict[str, Any]],
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=sorts_risk_level,
        sorts_suggestions=sorts_suggestions,
    )
    assert result["data"]["updateToeLinesSorts"]["success"]
    result = await query_get(user=user_email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test@test.com",
                    "attackedLines": 23,
                    "bePresent": False,
                    "bePresentUntil": "2021-01-19T15:41:04+00:00",
                    "comments": "comment 1",
                    "lastAuthor": "customer1@gmail.com",
                    "filename": "test/test#.config",
                    "firstAttackAt": "2020-01-19T15:41:04+00:00",
                    "loc": 4324,
                    "lastCommit": "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "universe"},
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                    "sortsSuggestions": None,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OT"
                "AjRklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
            },
            {
                "node": {
                    "attackedAt": "2021-02-20T05:00:00+00:00",
                    "attackedBy": "test2@test.com",
                    "attackedLines": 4,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 2",
                    "lastAuthor": "customer2@gmail.com",
                    "filename": "test2/test.sh",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 180,
                    "lastCommit": "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": sorts_risk_level,
                    "sortsSuggestions": sorts_suggestions,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
                "EjRklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
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
                    "filename": "test3/test.config",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "lastCommit": "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                    "sortsSuggestions": None,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
                "EjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9P"
            "VCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEj"
            "RklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(("sorts_risk_level"), ((-10), (-1), (101), (1000)))
async def test_update_toe_lines_sorts_range_fail(
    populate: bool, sorts_risk_level: int
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=sorts_risk_level,
        sorts_suggestions=[],
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidSortsRiskLevel.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
async def test_update_toe_lines_sorts_no_filename(populate: bool) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="non_existing_filename",
        sorts_risk_level=10,
        sorts_suggestions=[],
    )
    assert (
        result["errors"][0]["message"]
        == "Exception - Toe lines has not been found"
    )
