# pylint: disable=import-error
from aniso8601 import (
    parse_datetime,
)
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from comments import (
    domain as comments_domain,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventNotFound,
    InvalidCommentParent,
    InvalidFileSize,
    InvalidFileType,
    UnsanitizedInputFound,
)
from custom_types import (
    AddEventPayload,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventEvidenceType,
    EventSolutionReason,
    EventStateStatus,
)
from db_model.events.types import (
    Event,
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


async def test_get_event() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "418900971"
    test_data: Event = await loaders.event.load(event_id)
    expected_output = "unittesting"
    assert test_data.group_name == expected_output
    with pytest.raises(EventNotFound):
        await loaders.event.load("000001111")


@pytest.mark.changes_db
async def test_add_event() -> None:
    attrs = {
        "accessibility": ["VPN_CONNECTION"],
        "context": "OTHER",
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
        "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
    }
    event_payload = await events_domain.add_event(
        get_new_context(),
        hacker_email="unittesting@fluidattacks.com",
        group_name="unittesting",
        **attrs,
    )
    assert event_payload.success


@pytest.mark.changes_db
async def test_add_event_file_image() -> None:
    attrs = {
        "accessibility": ["VPN_CONNECTION"],
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
        "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
    }
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    imagename = os.path.dirname(os.path.abspath(__file__))
    imagename = os.path.join(imagename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, "text/csv"
        )
        with open(imagename, "rb") as image_test:
            uploaded_image = UploadFile(
                "test-anim.gif", image_test, "image/gif"
            )
            test_data = await events_domain.add_event(
                get_new_context(),
                hacker_email="unittesting@fluidattacks.com",
                group_name="unittesting",
                file=uploaded_file,
                image=uploaded_image,
                **attrs,
            )
    assert isinstance(test_data, AddEventPayload)
    assert test_data.success


@pytest.mark.changes_db
async def test_solve_event() -> None:
    request = await create_dummy_session("unittesting@fluidattacks.com")
    info = create_dummy_info(request)
    await events_domain.solve_event(
        info=info,
        event_id="538745942",
        hacker_email="unittesting@fluidattacks.com",
        date=parse_datetime("2019-12-09T05:00:00.000Z"),
        reason=EventSolutionReason.PERMISSION_GRANTED,
        other="Other info",
    )
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load("538745942")
    assert event.state.status == EventStateStatus.SOLVED
    assert event.state.other == "Other info"
    assert event.state.reason == EventSolutionReason.PERMISSION_GRANTED

    request = await create_dummy_session("unittesting@fluidattacks.com")
    info = create_dummy_info(request)
    with pytest.raises(EventAlreadyClosed):
        assert await events_domain.solve_event(
            info=info,
            event_id="538745942",
            hacker_email="unittesting@fluidattacks.com",
            date=parse_datetime("2019-12-09T05:00:00.000Z"),
            reason=None,
            other=None,
        )


@pytest.mark.changes_db
async def test_add_comment() -> None:
    event_id = "538745942"
    user_email = "integratesmanager@gmail.com"
    comment_id = str(round(time() * 1000))
    parent_comment = "0"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    comment_data = {
        "comment_type": "event",
        "parent": parent_comment,
        "content": "comment test",
        "comment_id": comment_id,
    }
    comment_id, success = await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent_comment
    )
    assert success
    assert comment_id

    comment_data["content"] = "comment test 2"
    comment_data["parent"] = comment_id
    comment_data["comment_id"] = str(round(time() * 1000))
    comment_id, success = await events_domain.add_comment(
        info,
        user_email,
        comment_data,
        event_id,
        parent_comment=str(comment_id),
    )
    assert success
    assert comment_id

    with pytest.raises(InvalidCommentParent):
        comment_data["parent"] = str(int(comment_id) + 1)
        comment_data["comment_id"] = str(round(time() * 1000))
        assert await events_domain.add_comment(
            info,
            user_email,
            comment_data,
            event_id,
            parent_comment=str(int(comment_id) + 1),
        )


@pytest.mark.changes_db
async def test_update_evidence() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "418900978"
    evidence_type = EventEvidenceType.FILE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
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

    loaders.event.clear(event_id)
    event_updated: Event = await loaders.event.load(event_id)
    assert (
        event_updated.evidences.file.file_name
        == "oneshottest-418900978-evidence_file.csv"
    )


async def test_update_evidence_invalid_id() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "=malicious-code-here"
    evidence_type = EventEvidenceType.FILE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
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
    evidence_type = EventEvidenceType.FILE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
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
    evidence_type = EventEvidenceType.IMAGE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, "text/csv"
        )
        with pytest.raises(InvalidFileType):
            await events_domain.validate_evidence(evidence_type, uploaded_file)


async def test_validate_evidence_invalid_file_size() -> None:
    evidence_type = EventEvidenceType.IMAGE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-big-image.jpg")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-big-image.jpg", test_file, "image/jpg"
        )
        with pytest.raises(InvalidFileSize):
            await events_domain.validate_evidence(evidence_type, uploaded_file)


@pytest.mark.changes_db
async def test_mask_event() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    event_id = "418900971"
    parent_comment = "0"
    comment_id = str(round(time() * 1000))
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    comment_data = {
        "comment_type": "event",
        "parent": "0",
        "content": "comment test",
        "comment_id": comment_id,
    }
    comment_id, success = await events_domain.add_comment(
        info,
        "integratesmanager@gmail.com",
        comment_data,
        event_id,
        parent_comment,
    )
    evidence_type = EventEvidenceType.FILE
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
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
    evidence_prefix = f"unittesting/{event_id}"

    assert success
    assert len(await comments_domain.get("event", event_id)) >= 1
    assert len(await events_domain.search_evidence(evidence_prefix)) >= 1

    loaders = get_new_context()
    test_data = await events_domain.mask(loaders, event_id)
    expected_output = True

    assert isinstance(test_data, bool)
    assert test_data == expected_output
    assert len(await comments_domain.get("event", event_id)) == 0
    assert len(await events_domain.search_evidence(evidence_prefix)) == 0
    new_loaders = get_new_context()
    event: Event = await new_loaders.event.load(event_id)
    assert event.description == "Masked"
