# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
    query_get,
)
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_refresh_toe_lines(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    group_name = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, group_name=group_name, monkeypatch=monkeypatch
    )
    assert result["data"]["refreshToeLines"]["success"]
    result = await query_get(user=email, group_name=group_name)
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": None,
                    "attackedBy": "",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "",
                    "filename": "back/mock.py",
                    "firstAttackAt": None,
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "6e119ae968656c52bfe85f80329c6b8400fb7921",
                    "loc": 10,
                    "modifiedDate": "2021-11-10T16:31:38+00:00",
                    "seenAt": "2021-11-10T20:35:20.372236+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjYmFjay9tb2NrLnB5In0=",
            },
            {
                "node": {
                    "attackedAt": None,
                    "attackedBy": "",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "",
                    "filename": "back/src/mock.py",
                    "firstAttackAt": None,
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "6e119ae968656c52bfe85f80329c6b8400fb7921",
                    "loc": 6,
                    "modifiedDate": "2021-11-10T16:31:38+00:00",
                    "seenAt": "2021-11-10T20:35:20.372236+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjYmFjay9zcmMvbW9jay5weSJ9",
            },
            {
                "node": {
                    "attackedAt": None,
                    "attackedBy": "",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "",
                    "filename": "front/mock.css",
                    "firstAttackAt": None,
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "6e4a6706dff4332a73251e4f2e7fbf67025f369e",
                    "loc": 7,
                    "modifiedDate": "2021-11-10T20:40:44+00:00",
                    "seenAt": "2021-11-10T20:35:20.372236+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjZnJvbnQvbW9jay5jc3MifQ==",
            },
            {
                "node": {
                    "attackedAt": None,
                    "attackedBy": "",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "",
                    "filename": "front/mock.js",
                    "firstAttackAt": None,
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "3ca2ffbfeae4f2df16810359a9363231fabc1750",
                    "loc": 8,
                    "modifiedDate": "2021-11-10T16:32:24+00:00",
                    "seenAt": "2021-11-10T20:35:20.372236+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjZnJvbnQvbW9jay5qcyJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test@test.com",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 1",
                    "filename": "test1/test.sh",
                    "firstAttackAt": "2020-01-19T15:41:04+00:00",
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "50a516954a321f95c6fb8baccb640e87d2f5d193",
                    "loc": 8,
                    "modifiedDate": "2021-11-11T17:41:46+00:00",
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjdGVzdDEvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test3@test.com",
                    "attackedLines": 120,
                    "bePresent": False,
                    "bePresentUntil": "2021-11-10T20:35:20.372236+00:00",
                    "comments": "comment 3",
                    "filename": "test3/test.sh",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "lastAuthor": "customer3@gmail.com",
                    "lastCommit": "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
                    "loc": 243,
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjdGVzdDMvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-12-20T05:00:00+00:00",
                    "attackedBy": "test4@test.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 4",
                    "filename": "test4/test.sh",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "50a516954a321f95c6fb8baccb640e87d2f5d193",
                    "loc": 8,
                    "modifiedDate": "2021-11-11T17:41:46+00:00",
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjdGVzdDQvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": None,
                    "attackedBy": "test5@test.com",
                    "attackedLines": 0,
                    "bePresent": True,
                    "bePresentUntil": None,
                    "comments": "comment 5",
                    "filename": "test5/test.sh",
                    "firstAttackAt": None,
                    "lastAuthor": "authoremail@test.com",
                    "lastCommit": "50a516954a321f95c6fb8baccb640e87d2f5d193",
                    "loc": 7,
                    "modifiedDate": "2021-11-11T17:41:46+00:00",
                    "seenAt": "2019-01-02T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5B"
                "TUUjdGVzdDUvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-02-20T05:00:00+00:00",
                    "attackedBy": "test2@test.com",
                    "attackedLines": 4,
                    "bePresent": False,
                    "bePresentUntil": "2021-11-10T20:35:20.372236+00:00",
                    "comments": "comment 2",
                    "filename": "test2/test#.config",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "lastAuthor": "customer2@gmail.com",
                    "lastCommit": "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    "loc": 180,
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": 80,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9"
                "PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjRklMRU5B"
                "TUUjdGVzdDIvdGVzdCMuY29uZmlnIn0=",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9P"
            "VCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjRklMRU5BTUUjd"
            "GVzdDIvdGVzdCMuY29uZmlnIn0=",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["service_forces@fluidattacks.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_refresh_toe_lines_fail(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, group_name="group1", monkeypatch=monkeypatch
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
