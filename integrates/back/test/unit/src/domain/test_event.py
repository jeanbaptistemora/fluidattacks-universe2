from custom_exceptions import (
    InvalidFileName,
    InvalidFileSize,
    InvalidFileType,
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from events import (
    domain as events_domain,
)
from newutils import (
    datetime as datetime_utils,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_update_evidence_invalid_id() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "=malicious-code-here"
    evidence_type = EventEvidenceId.FILE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, "text/csv"
        )
        with pytest.raises(UnsanitizedInputFound):
            await events_domain.update_evidence(
                loaders,
                event_id,
                evidence_type,
                uploaded_file,
                datetime_utils.get_now(),
            )


async def test_update_evidence_invalid_filename() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "418900978"
    evidence_type = EventEvidenceId.FILE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "malicious;-code,-here.csv", test_file, "text/csv"
        )
        with pytest.raises(UnsanitizedInputFound):
            await events_domain.update_evidence(
                loaders,
                event_id,
                evidence_type,
                uploaded_file,
                datetime_utils.get_now(),
            )


async def test_validate_evidence_invalid_image_type() -> None:
    evidence_type = EventEvidenceId.IMAGE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load("unittesting")
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, "text/csv"
        )
        with pytest.raises(InvalidFileType):
            await events_domain.validate_evidence(
                group_name=group.name.lower(),
                organization_name=organization.name.lower(),
                evidence_id=evidence_type,
                file=uploaded_file,
            )


async def test_validate_evidence_invalid_file_size() -> None:
    evidence_type = EventEvidenceId.IMAGE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-big-image.jpg")
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load("unittesting")
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-big-image.jpg", test_file, "image/jpg"
        )
        with pytest.raises(InvalidFileSize):
            await events_domain.validate_evidence(
                group_name=group.name.lower(),
                organization_name=organization.name.lower(),
                evidence_id=evidence_type,
                file=uploaded_file,
            )


async def test_validate_evidence_invalid_name() -> None:
    evidence_type = EventEvidenceId.FILE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load("unittesting")
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-records.csv", test_file, "text/csv"
        )
        with pytest.raises(InvalidFileName):
            await events_domain.validate_evidence(
                group_name=group.name.lower(),
                organization_name=organization.name.lower(),
                evidence_id=evidence_type,
                file=uploaded_file,
            )
