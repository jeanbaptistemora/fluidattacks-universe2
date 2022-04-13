from . import (
    get_result,
    query_get,
)
from .constants import (
    USERS_EMAILS,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(["email"], USERS_EMAILS)
async def test_update_toe_lines_sorts(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=10,
    )
    assert result["data"]["updateToeLinesSorts"]["success"]
    result = await query_get(user=email, group_name="group1")
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
                    "lastCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "product"},
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
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
                    "loc": 8,
                    "lastCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": 10,
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
                    "lastCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
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


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(["email"], USERS_EMAILS)
async def test_update_toe_lines_sorts_no_filename(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_nickname="asm_1",
        filename="non_existing_filename",
        sorts_risk_level=10,
    )
    assert (
        result["errors"][0]["message"]
        == "Exception - Toe lines has not been found"
    )
