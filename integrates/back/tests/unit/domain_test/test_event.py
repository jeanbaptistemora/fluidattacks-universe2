from aniso8601 import (
    parse_datetime,
)
from back.tests.unit.utils import (
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
)
from dataloaders import (
    get_new_context,
)
from events import (
    dal as events_dal,
    domain as events_domain,
)
from graphql.type import (
    GraphQLResolveInfo,
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
    event_id = "418900971"
    test_data = await events_domain.get_event(event_id)
    expected_output = "unittesting"
    assert test_data.get("group_name") == expected_output
    with pytest.raises(EventNotFound):
        await events_domain.get_event("000001111")


@pytest.mark.changes_db
async def test_add_event() -> None:
    attrs = {
        "action_after_blocking": "TRAINING",
        "action_before_blocking": "DOCUMENT_GROUP",
        "accessibility": "REPOSITORY",
        "context": "OTHER",
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "CLIENT_DETECTS_ATTACK",
        "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
    }
    assert await events_domain.add_event(
        get_new_context(),
        hacker_email="unittesting@fluidattacks.com",
        group_name="unittesting",
        **attrs,
    )


@pytest.mark.changes_db
async def test_add_event_file_image() -> None:
    attrs = {
        "action_after_blocking": "TRAINING",
        "action_before_blocking": "DOCUMENT_GROUP",
        "accessibility": "REPOSITORY",
        "context": "OTHER",
        "detail": "Something happened.",
        "event_date": parse_datetime("2019-12-09T05:00:00.000Z"),
        "event_type": "CLIENT_DETECTS_ATTACK",
    }
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    imagename = os.path.dirname(os.path.abspath(__file__))
    imagename = os.path.join(imagename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "text/csv")
        with open(imagename, "rb") as image_test:
            uploaded_image = UploadFile(
                image_test.name, image_test, "image/gif"
            )
            test_data = await events_domain.add_event(
                get_new_context(),
                hacker_email="unittesting@fluidattacks.com",
                group_name="unittesting",
                file=uploaded_file,
                image=uploaded_image,
                **attrs,
            )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output


@pytest.mark.changes_db
async def test_solve_event() -> None:
    assert await events_domain.solve_event(
        event_id="538745942",
        affectation=1,
        hacker_email="unittesting@fluidattacks.com",
        date=parse_datetime("2019-12-09T05:00:00.000Z"),
    )
    event = await events_domain.get_event("538745942")
    assert event["historic_state"][-1]["state"] == "SOLVED"
    with pytest.raises(EventAlreadyClosed):
        assert await events_domain.solve_event(
            event_id="538745942",
            affectation=1,
            hacker_email="unittesting@fluidattacks.com",
            date=parse_datetime("2019-12-09T05:00:00.000Z"),
        )


@pytest.mark.changes_db
async def test_add_comment() -> None:
    event_id = "538745942"
    user_email = "integratesmanager@gmail.com"
    comment_id = str(round(time() * 1000))
    parent = "0"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
    comment_data = {
        "comment_type": "event",
        "parent": parent,
        "content": "comment test",
        "comment_id": comment_id,
    }
    comment_id, success = await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent
    )
    assert success
    assert comment_id

    comment_data["content"] = "comment test 2"
    comment_data["parent"] = comment_id
    comment_data["comment_id"] = str(round(time() * 1000))
    comment_id, success = await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent=str(comment_id)
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
            parent=str(int(comment_id) + 1),
        )


@pytest.mark.changes_db
async def test_update_evidence() -> None:
    event_id = "418900978"
    evidence_type = "records"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "text/csv")
        test_data = await events_domain.update_evidence(
            event_id,
            evidence_type,
            uploaded_file,
            datetime_utils.get_now(),
        )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output


async def test_validate_evidence_invalid_image_type() -> None:
    evidence_type = "evidence"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "text/csv")
        with pytest.raises(InvalidFileType):
            await events_domain.validate_evidence(evidence_type, uploaded_file)


async def test_validate_evidence_invalid_file_size() -> None:
    evidence_type = "evidence"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-big-image.jpg")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "image/jpg")
        with pytest.raises(InvalidFileSize):
            await events_domain.validate_evidence(evidence_type, uploaded_file)


@pytest.mark.changes_db
async def test_mask_event() -> None:
    event_id = "418900971"
    parent = "0"
    comment_id = str(round(time() * 1000))
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
    comment_data = {
        "comment_type": "event",
        "parent": "0",
        "content": "comment test",
        "comment_id": comment_id,
    }
    comment_id, success = await events_domain.add_comment(
        info, "integratesmanager@gmail.com", comment_data, event_id, parent
    )
    evidence_type = "records"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "text/csv")
        await events_domain.update_evidence(
            event_id,
            evidence_type,
            uploaded_file,
            datetime_utils.get_now(),
        )
    evidence_prefix = f"unittesting/{event_id}"

    assert success
    assert len(await comments_domain.get("event", event_id)) >= 1
    assert len(await events_dal.search_evidence(evidence_prefix)) >= 1

    test_data = await events_domain.mask(event_id)
    expected_output = True

    assert isinstance(test_data, bool)
    assert test_data == expected_output
    assert len(await comments_domain.get("event", event_id)) == 0
    assert len(await events_dal.search_evidence(evidence_prefix)) == 0

    event = await events_domain.get_event(event_id)
    assert event.get("detail") == "Masked"
