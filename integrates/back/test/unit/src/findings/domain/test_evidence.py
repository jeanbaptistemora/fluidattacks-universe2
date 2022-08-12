from collections import (
    OrderedDict,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
    validate_evidence,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)

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


async def test_validate_evidence_records() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/test-file-records.csv")
    mime_type = "text/csv"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        test_data = await validate_evidence(evidence_id, uploaded_file)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output
