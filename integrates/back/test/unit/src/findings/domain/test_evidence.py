from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
)
from collections import (
    OrderedDict,
)
from custom_exceptions import (
    InvalidFileName,
    InvalidFileType,
)
from dataloaders import (
    get_new_context,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
    validate_evidence,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


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
@patch(
    get_mocked_path("findings_storage.search_evidence"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("findings_storage.download_evidence"),
    new_callable=AsyncMock,
)
async def test_download_evidence_file(
    mock_download_evidence: AsyncMock,
    mock_search_evidence: AsyncMock,
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


@pytest.mark.parametrize(
    ["group_name", "finding_id", "file_name", "expected_output"],
    [
        [
            "unittesting",
            "422286126",
            "unittesting-422286126-evidence_file.csv",
            [
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
                    [
                        ("song", "hysteria"),
                        ("artist", "def leppard"),
                        ("year", "1987"),
                    ]
                ),
            ],
        ],
    ],
)
@patch(get_mocked_path("download_evidence_file"), new_callable=AsyncMock)
async def test_get_records_from_file(
    mock_download_evidence_file: AsyncMock,
    group_name: str,
    finding_id: str,
    file_name: str,
    expected_output: list[dict[object, object]],
) -> None:
    mock_download_evidence_file.return_value = get_mock_response(
        get_mocked_path("download_evidence_file"),
        json.dumps([group_name, finding_id, file_name]),
    )

    test_data = await get_records_from_file(group_name, finding_id, file_name)

    assert test_data == expected_output
    assert mock_download_evidence_file.called is True


async def test_validate_evidence_records() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/evidences/test-file-records.csv")
    mime_type = "text/csv"
    finding_id = "463558592"
    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        test_data = await validate_evidence(
            evidence_id=evidence_id,
            file=uploaded_file,
            loaders=loaders,
            finding=finding,
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
    finding = await loaders.finding.load(finding_id)
    assert finding
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        with pytest.raises(InvalidFileType):
            await validate_evidence(
                evidence_id=evidence_id,
                file=uploaded_file,
                loaders=loaders,
                finding=finding,
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
    finding = await loaders.finding.load(finding_id)
    assert finding
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.png", test_file, mime_type
        )
        with pytest.raises(InvalidFileName):
            await validate_evidence(
                evidence_id=evidence_id,
                file=uploaded_file,
                loaders=loaders,
                finding=finding,
                validate_name=True,
            )

    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-0123456789.png", test_file, mime_type
        )
        test_data = await validate_evidence(
            evidence_id=evidence_id,
            file=uploaded_file,
            loaders=loaders,
            finding=finding,
            validate_name=True,
        )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output
