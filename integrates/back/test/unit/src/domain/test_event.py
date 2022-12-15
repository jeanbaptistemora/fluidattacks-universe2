# pylint: disable=import-error
from aniso8601 import (
    parse_datetime,
)
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventNotFound,
    InvalidCommentParent,
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
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
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


@pytest.mark.changes_db
async def test_add_event() -> None:
    attrs = {
        "context": "OTHER",
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
        "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
    }
    event_id = await events_domain.add_event(
        get_new_context(),
        hacker_email="unittesting@fluidattacks.com",
        group_name="unittesting",
        **attrs,
    )
    loaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.id == event_id
    assert event.hacker == "unittesting@fluidattacks.com"
    assert event.type == EventType.AUTHORIZATION_SPECIAL_ATTACK


@pytest.mark.changes_db
async def test_add_event_file_image() -> None:
    attrs = {
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
        "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
    }
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/test-file-records.csv")
    imagename = os.path.dirname(os.path.abspath(__file__))
    imagename = os.path.join(imagename, "./mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-0123456789.csv", test_file, "text/csv"
        )
        with open(imagename, "rb") as image_test:
            uploaded_image = UploadFile(
                "okada-unittesting-0987654321.gif", image_test, "image/gif"
            )
            test_data = await events_domain.add_event(
                get_new_context(),
                hacker_email="unittesting@fluidattacks.com",
                group_name="unittesting",
                file=uploaded_file,
                image=uploaded_image,
                **attrs,
            )
    assert isinstance(test_data, str)


@pytest.mark.changes_db
async def test_solve_event() -> None:
    request = await create_dummy_session("unittesting@fluidattacks.com")
    info = create_dummy_info(request)
    await events_domain.solve_event(
        info=info,
        event_id="538745942",
        hacker_email="unittesting@fluidattacks.com",
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
            reason=None,  # type: ignore
            other=None,
        )


@pytest.mark.changes_db
async def test_add_comment() -> None:
    event_id = "538745942"
    user_email = "integratesmanager@gmail.com"
    comment_id = str(round(time() * 1000))
    parent_comment = "0"
    today = datetime_utils.get_utc_now()
    comment_data = EventComment(
        event_id=event_id,
        parent_id=parent_comment,
        creation_date=today,
        content="comment test",
        id=comment_id,
        email=user_email,
        full_name="integrates manager",
    )
    await events_domain.add_comment(
        get_new_context(), comment_data, user_email, event_id, parent_comment
    )
    loaders = get_new_context()
    event_comments: tuple[
        EventComment, ...
    ] = await loaders.event_comments.load(event_id)
    assert event_comments[-1].id == comment_id
    assert event_comments[-1].event_id == event_id
    assert event_comments[-1].content == "comment test"

    new_comment_data = EventComment(
        event_id=event_id,
        parent_id=comment_id,
        creation_date=today,
        content="comment test 2",
        id=str(round(time() * 1000)),
        email=user_email,
        full_name="integrates manager",
    )
    await events_domain.add_comment(
        get_new_context(),
        new_comment_data,
        user_email,
        event_id,
        parent_comment=str(comment_id),
    )
    new_loaders = get_new_context()
    new_event_comments: list[
        EventComment
    ] = await new_loaders.event_comments.load(event_id)
    assert new_event_comments[-1].id == new_comment_data.id
    assert new_event_comments[-1].event_id == event_id
    assert new_event_comments[-1].content == "comment test 2"
    assert new_event_comments[-1].parent_id == comment_id

    with pytest.raises(InvalidCommentParent):
        inv_comment_data = new_comment_data._replace(
            parent_id=str(int(comment_id) + 1),
            id=str(round(time() * 1000)),
        )
        assert await events_domain.add_comment(  # type: ignore
            get_new_context(),
            inv_comment_data,
            user_email,
            event_id,
            parent_comment=str(int(comment_id) + 1),
        )


@pytest.mark.changes_db
async def test_update_evidence() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "418900978"
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

    loaders.event.clear(event_id)
    event_updated: Event = await loaders.event.load(event_id)
    assert (
        event_updated.evidences.file_1.file_name  # type: ignore
        == "oneshottest_418900978_evidence_file_1.csv"
    )


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
