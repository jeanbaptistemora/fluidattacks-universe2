# pylint: disable=import-error
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from collections import (
    OrderedDict,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from custom_exceptions import (
    InvalidFileName,
    InvalidFileType,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
    validate_evidence,
)
import json
from mypy_boto3_s3 import (
    S3Client,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]

BUCKET_NAME = FI_AWS_S3_MAIN_BUCKET


async def test_create_test_bucket(s3_mock: S3Client) -> None:
    result = s3_mock.list_buckets()
    assert len(result["Buckets"]) == 1
    assert result["Buckets"][0]["Name"] == FI_AWS_S3_MAIN_BUCKET


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
    file_location = os.path.join(file_location, "mock/evidences/" + file_name)
    file_name = "/".join(
        ["evidences", group_name.lower(), finding_id, file_name]
    )
    with open(file_location, "rb") as data:
        s3_mock.upload_fileobj(data, BUCKET_NAME, file_name)
    assert bool(s3_mock.get_object(Bucket=BUCKET_NAME, Key=file_name))


@mock.patch(
    get_mocked_path("findings_storage.search_evidence"),
    new_callable=mock.AsyncMock,
)
@mock.patch(
    get_mocked_path("findings_storage.download_evidence"),
    new_callable=mock.AsyncMock,
)
@pytest.mark.parametrize(
    [
        "group_name",
        "finding_id",
        "file_name",
    ],
    [
        [
            "unittesting",
            "422286126",
            "unittesting-422286126-evidence_route_1.png",
        ],
    ],
)
async def test_download_evidence_file(
    mock_download_evidence: mock.AsyncMock,
    mock_search_evidence: mock.AsyncMock,
    group_name: str,
    finding_id: str,
    file_name: str,
) -> None:
    mock_parameters = json.dumps([group_name, finding_id, file_name])
    mock_search_evidence.return_value = get_mock_response(
        get_mocked_path("findings_storage.search_evidence"), mock_parameters
    )
    mock_download_evidence.return_value = get_mock_response(
        get_mocked_path("findings_storage.download_evidence"), mock_parameters
    )
    test_data = await download_evidence_file(group_name, finding_id, file_name)

    expected_output = os.path.abspath(
        # FP: local testing
        "/tmp/unittesting-422286126-evidence_route_1.png"  # NOSONAR
    )
    assert test_data == expected_output


@pytest.mark.skip(reason="Test failing when using cloud s3")
@mock.patch(
    "s3.operations.get_s3_resource",
    new_callable=mock.AsyncMock,
)
async def test_get_records_from_file(
    mock_s3_resource: mock.AsyncMock, s3_mock: S3Client
) -> None:
    def mock_download_file(*args: Any) -> Any:
        return s3_mock.download_file(*args)

    def mock_list_objects_v2(**kwargs: Any) -> Any:
        return s3_mock.list_objects_v2(**kwargs)

    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_file.csv"
    mock_s3_resource.return_value.download_file.side_effect = (
        mock_download_file
    )
    mock_s3_resource.return_value.list_objects_v2.side_effect = (
        mock_list_objects_v2
    )
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
    filename = os.path.join(filename, "mock/evidences/test-file-records.csv")
    mime_type = "text/csv"
    finding_id = "463558592"
    loaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        test_data = await validate_evidence(
            evidence_id, uploaded_file, loaders, finding
        )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output


async def test_validate_evidence_records_invalid_type() -> None:
    loaders = get_new_context()
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(
        filename, "mock/evidences/unittesting-422286126-evidence_route_1.png"
    )
    mime_type = "image/png"
    finding_id = "422286126"
    finding: Finding = await loaders.finding.load(finding_id)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        with pytest.raises(InvalidFileType):
            await validate_evidence(
                evidence_id, uploaded_file, loaders, finding
            )


async def test_validate_evidence_records_invalid_name() -> None:
    loaders = get_new_context()
    evidence_id = "evidence_route_1"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(
        filename, "mock/evidences/unittesting-422286126-evidence_route_1.png"
    )
    mime_type = "image/png"
    finding_id = "422286126"
    finding: Finding = await loaders.finding.load(finding_id)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.png", test_file, mime_type
        )
        with pytest.raises(InvalidFileName):
            await validate_evidence(
                evidence_id,
                uploaded_file,
                loaders,
                finding,
                validate_name=True,
            )

    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-0123456789.png", test_file, mime_type
        )
        test_data = await validate_evidence(
            evidence_id,
            uploaded_file,
            loaders,
            finding,
            validate_name=True,
        )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output
