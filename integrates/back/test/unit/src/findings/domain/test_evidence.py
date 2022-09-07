# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from collections import (
    OrderedDict,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
    validate_evidence,
)
from mypy_boto3_s3 import (
    S3Client,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]

BUCKET_NAME = "test_bucket"


async def test_create_test_bucket(s3_mock: S3Client) -> None:
    result = s3_mock.list_buckets()
    assert len(result["Buckets"]) == 1
    assert result["Buckets"][0]["Name"] == "test_bucket"


@pytest.mark.parametrize(
    [
        "group_name",
        "file_name",
        "finding_id",
    ],
    [
        [
            "unittesting",
            "unittesting-422286126-evidence_route_1.png",
            "422286126",
        ],
        [
            "unittesting",
            "unittesting-422286126-evidence_file.csv",
            "422286126",
        ],
    ],
)
async def test_upload_test_file(
    group_name: str, file_name: str, finding_id: str, s3_mock: S3Client
) -> None:
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    file_name = "/".join([group_name.lower(), finding_id, file_name])
    with open(file_location, "rb") as data:
        s3_mock.upload_fileobj(data, BUCKET_NAME, file_name)
    assert bool(s3_mock.get_object(Bucket=BUCKET_NAME, Key=file_name))


async def test_download_evidence_file(s3_mock: S3Client) -> None:
    def side_effect(bucket: str, file_name: str, file_path: str) -> None:
        if bool(bucket and file_name and file_path):
            s3_mock.download_file(BUCKET_NAME, file_name, file_path)

    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_route_1.png"
    file_key = "/".join([group_name.lower(), finding_id, file_name])
    with mock.patch("s3.operations.download_file") as mock_download:
        mock_download.side_effect = side_effect
        with mock.patch(
            "findings.storage.search_evidence"
        ) as mock_search_evidence:
            mock_search_evidence.return_value = bool(
                s3_mock.get_object(Bucket=BUCKET_NAME, Key=file_key)
            )
            test_data = await download_evidence_file(
                group_name, finding_id, file_name
            )

    expected_output = os.path.abspath(
        # FP: local testing
        "/tmp/unittesting-422286126-evidence_route_1.png"  # NOSONAR
    )
    assert test_data == expected_output


async def test_get_records_from_file(s3_mock: S3Client) -> None:
    def side_effect(bucket: str, file_name: str, file_path: str) -> None:
        if bool(bucket and file_name and file_path):
            s3_mock.download_file(BUCKET_NAME, file_name, file_path)

    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_file.csv"
    file_key = "/".join([group_name.lower(), finding_id, file_name])
    with mock.patch("s3.operations.download_file") as mock_download:
        mock_download.side_effect = side_effect
        with mock.patch(
            "findings.storage.search_evidence"
        ) as mock_search_evidence:
            mock_search_evidence.return_value = bool(
                s3_mock.get_object(Bucket=BUCKET_NAME, Key=file_key)
            )
            test_data = await get_records_from_file(
                group_name, finding_id, file_name
            )
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
                ("year", "nirvana"),
            ]
        ),
        OrderedDict(
            [("song", "zenith"), ("artist", "zenith"), ("year", "2015")]
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
