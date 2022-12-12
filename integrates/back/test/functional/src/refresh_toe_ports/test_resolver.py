from . import (
    query_get,
    refresh_toe_ports,
)
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from freezegun import (
    freeze_time,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_ports")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_refresh_toe_ports(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    group_name = "group1"
    await refresh_toe_ports(
        user=email,
        group_name=group_name,
        monkeypatch=monkeypatch,
    )
    result = await query_get(user=email, group_name=group_name)
    assert result["data"]["group"]["toePorts"] == {
        "edges": [
            {
                "cursor": (
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk"
                    "9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2O"
                    "TAjQUREUkVTUyMxOTIuMTY4LjEuMSNQT1JUIzgwODAifQ=="
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
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk9PVCM"
                    "2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjQUREUk"
                    "VTUyMxOTIuMTY4LjEuMSNQT1JUIzgwODEifQ=="
                ),
                "node": {
                    "address": "192.168.1.1",
                    "attackedAt": "2020-01-02T05:00:00+00:00",
                    "attackedBy": "admin@gmail.com",
                    "bePresent": True,
                    "bePresentUntil": None,
                    "firstAttackAt": "2020-01-02T05:00:00+00:00",
                    "hasVulnerabilities": False,
                    "port": 8081,
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
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk9PVCM3"
                    "NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjQUREUkVT"
                    "UyMxOTIuMTY4LjEuMiNQT1JUIzgwODAifQ=="
                ),
                "node": {
                    "address": "192.168.1.2",
                    "attackedAt": "2021-02-11T05:00:00+00:00",
                    "attackedBy": "admin@gmail.com",
                    "bePresent": False,
                    "bePresentUntil": "2021-11-10T20:35:20.372236+00:00",
                    "firstAttackAt": "2021-02-11T05:00:00+00:00",
                    "hasVulnerabilities": False,
                    "port": 8080,
                    "root": {
                        "__typename": "IPRoot",
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "root2",
                    },
                    "seenAt": "2020-01-11T05:00:00+00:00",
                    "seenFirstTimeBy": "test2@test.com",
                },
            },
            {
                "cursor": (
                    "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk9PVCM3"
                    "NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjQUREUkVT"
                    "UyMxOTIuMTY4LjEuMiNQT1JUIzgwODEifQ=="
                ),
                "node": {
                    "address": "192.168.1.2",
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
                "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiUE9SVFMjUk"
                "9PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjQU"
                "REUkVTUyMxOTIuMTY4LjEuMiNQT1JUIzgwODEifQ=="
            ),
            "hasNextPage": False,
        },
    }
