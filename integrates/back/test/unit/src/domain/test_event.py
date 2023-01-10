from custom_exceptions import (
    EventNotFound,
    InvalidFileName,
    InvalidFileSize,
    InvalidFileType,
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.event_comments.types import (
    EventComment,
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
from time import (
    time,
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


@pytest.mark.changes_db
async def test_remove_event() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "48192579"
    group_name = "deletegroup"
    parent_comment = "0"
    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_utc_now()
    comment_data = EventComment(
        event_id=event_id,
        parent_id=parent_comment,
        creation_date=today,
        content="comment test",
        id=comment_id,
        email="unittest@fluidattacks.com",
        full_name="unit test",
    )
    await events_domain.add_comment(
        loaders,
        comment_data,
        "integratesmanager@gmail.com",
        event_id,
        parent_comment,
    )
    evidence_type = EventEvidenceId.FILE_1
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, "text/csv"
        )
        await events_domain.update_evidence(
            loaders,
            event_id,
            evidence_type,
            uploaded_file,
            datetime_utils.get_now(),
        )
    evidence_prefix = f"{group_name}/{event_id}"

    loaders = get_new_context()
    assert len(await loaders.event_comments.load(event_id)) >= 1
    assert len(await events_domain.search_evidence(evidence_prefix)) >= 1
    assert await loaders.event.load(event_id)

    await events_domain.remove_event(event_id, group_name)

    new_loaders = get_new_context()
    assert len(await new_loaders.event_comments.load(event_id)) == 0
    assert len(await events_domain.search_evidence(evidence_prefix)) == 0
    with pytest.raises(EventNotFound):
        await new_loaders.event.load(event_id)
