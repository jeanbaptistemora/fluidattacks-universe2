from collections import (
    OrderedDict,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
)
from newutils.vulnerabilities import (
    get_reattack_requester,
)
import os
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_download_evidence_file() -> None:
    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_route_1.png"
    test_data = await download_evidence_file(group_name, finding_id, file_name)
    expected_output = os.path.abspath(
        # FP: local testing
        "/tmp/unittesting-422286126-evidence_route_1.png"  # NOSONAR
    )
    assert test_data == expected_output


async def test_get_records_from_file() -> None:
    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_file.csv"
    test_data = await get_records_from_file(group_name, finding_id, file_name)
    expected_output = [
        OrderedDict(
            [
                ("song", "a million little pieces"),
                ("artist", "placebo"),
                ("year", "2010"),
            ]
        ),
        OrderedDict(
            [
                ("song", "heart shaped box"),
                ("artist", "nirvana"),
                ("year", "1992"),
            ]
        ),
        OrderedDict(
            [("song", "zenith"), ("artist", "ghost"), ("year", "2015")]
        ),
        OrderedDict(
            [("song", "hysteria"), ("artist", "def leppard"), ("year", "1987")]
        ),
    ]

    assert test_data == expected_output


async def test_get_reattack_requester() -> None:
    loaders = get_new_context()
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        "3bcdb384-5547-4170-a0b6-3b397a245465"
    )
    requester = await get_reattack_requester(
        loaders,
        vuln=vulnerability,
    )
    assert requester == "integratesuser@gmail.com"
