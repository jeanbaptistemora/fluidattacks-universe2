from . import (
    get_result,
    query_get,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-05-05T07:00:00+00:00")
async def test_update_toe_lines_attacked_lines_set_lines(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filename="test/test#.config",
        attacked_lines=8,
        comments="edited comments 1",
    )
    assert result["data"]["updateToeLinesAttackedLines"]["success"]
    result = await query_get(user=email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-05-05T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "edited comments 1",
                    "lastAuthor": "customer1@gmail.com",
                    "filename": "test/test#.config",
                    "firstAttackAt": "2021-05-05T07:00:00+00:00",
                    "loc": 4324,
                    "lastCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OT"
                "AjRklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9P"
            "VCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAj"
            "RklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-05-06T07:00:00+00:00")
async def test_update_toe_lines_attacked_lines_not_set_lines(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group2",
        root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
        filename="test2/test.sh",
        attacked_lines=None,
        comments="edited comments 2",
    )
    assert result["data"]["updateToeLinesAttackedLines"]["success"]
    result = await query_get(user=email, group_name="group2")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-05-06T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "edited comments 2",
                    "lastAuthor": "customer2@gmail.com",
                    "filename": "test2/test.sh",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "lastCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "asm_1",
                    },
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDIiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMW"
                "EjRklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDIiLCAic2siOiAiTElORVMjUk9P"
            "VCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEj"
            "RklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["architect@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
        ["user@fluidattacks.com"],
        ["user_manager@fluidattacks.com"],
        ["executive@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
        ["service_forces@fluidattacks.com"],
        ["architect@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["executive@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_update_toe_lines_attacked_lines_access_denied(
    populate: bool, email: str
) -> None:
    assert populate
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filename="test/test#.config",
        attacked_lines=8,
        comments="edited comments 1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-05-06T07:00:00+00:00")
async def test_update_toe_lines_attacked_lines_invalid_attacked_lines(
    populate: bool, email: str
) -> None:
    assert populate
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group3",
        root_id="86e9b0a8-b6be-4b3f-8006-a9a060f69e81",
        filename="test3/test.config",
        attacked_lines=5000,
        comments="edited comments 1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - The attacked lines must be between 1 and the loc "
        "(lines of code)"
    )
