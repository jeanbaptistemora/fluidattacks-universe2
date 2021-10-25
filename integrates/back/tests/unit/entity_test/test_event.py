from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
)
from newutils import (
    datetime as datetime_utils,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)

pytestmark = pytest.mark.asyncio


async def test_event() -> None:
    """Check for event."""
    query = """{
        event(identifier: "418900971"){
            client
            evidence
            groupName
            eventType
            detail
            eventDate
            eventStatus
            historicState
            affectation
            accessibility
            affectedComponents
            context
            subscription
            evidenceFile
            closingDate
            consulting {
                content
            }
            __typename
        }
    }"""
    data = {"query": query}
    request = await create_dummy_session()
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "event" in result["data"]
    assert result["data"]["event"]["groupName"] == "unittesting"
    assert result["data"]["event"]["detail"] == "Integrates unit test"


async def test_events() -> None:
    """Check for events."""
    query = """{
        events(groupName: "unittesting"){
            groupName
            detail
        }
    }"""
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "events" in result["data"]
    assert result["data"]["events"][0]["groupName"] == "unittesting"
    assert len(result["data"]["events"][0]["detail"]) >= 1


@pytest.mark.changes_db
async def test_create_event() -> None:
    """Check for addEvent mutation."""
    query = """
        mutation {
            addEvent(groupName: "unittesting",
                        actionAfterBlocking: TRAINING,
                        actionBeforeBlocking: DOCUMENT_GROUP,
                        accessibility: ENVIRONMENT,
                        context: CLIENT,
                        detail: "Test",
                        eventDate: "2020-02-01T00:00:00Z",
                        eventType: INCORRECT_MISSING_SUPPLIES
                        rootId: "4039d098-ffc5-4984-8ed3-eb17bca98e19"
            ) {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["addEvent"]


@pytest.mark.changes_db
async def test_solve_event() -> None:
    """Check for solveEvent mutation."""
    query = """
        mutation {
            solveEvent(eventId: "418900971",
                        affectation: "1",
                        date: "2020-02-01T00:00:00Z") {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    if "errors" not in result:
        assert "errors" not in result
        assert "success" in result["data"]["solveEvent"]
    else:
        assert (
            "The event has already been closed"
            in result["errors"][0]["message"]
        )


@pytest.mark.changes_db
async def test_add_event_consult() -> None:
    """Check for addEventConsult mutation."""
    query = """
        mutation {
            addEventConsult(eventId: "538745942",
                            parent: "0",
                            content: "Test comment") {
                success
                commentId
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session(
        username="integratesmanager@gmail.com"
    )
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["addEventConsult"]
    assert "commentId" in result["data"]["addEventConsult"]


@pytest.mark.changes_db
async def test_update_event_evidence() -> None:
    """Check for updateEventEvidence mutation."""
    query = """
        mutation updateEventEvidence(
            $eventId: String!,
            $evidenceType: EventEvidenceType!,
            $file: Upload!
        ) {
            updateEventEvidence(eventId: $eventId,
                                evidenceType: $evidenceType,
                                file: $file) {
                success
            }
        }
    """
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "image/gif")
        variables = {
            "eventId": "540462628",
            "evidenceType": "IMAGE",
            "file": uploaded_file,
        }
        data = {"query": query, "variables": variables}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)

    assert "errors" not in result
    assert "success" in result["data"]["updateEventEvidence"]

    date_str = datetime_utils.get_as_str(datetime_utils.get_now())
    query = """
        query GetEvent($eventId: String!) {
            event(identifier: $eventId) {
                evidence
                evidenceDate
            }
        }
    """
    variables = {"eventId": "540462628"}
    data = {"query": query, "variables": variables}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert result["data"]["event"]["evidence"] == (
        "unittesting-540462628-evidence.gif"
    )
    assert result["data"]["event"]["evidenceDate"].split(" ")[0] == (
        date_str.split(" ")[0]
    )


@pytest.mark.changes_db
async def test_download_event_file() -> None:
    """Check for downloadEventFile mutation."""
    query = """
        mutation {
            downloadEventFile(
                eventId: "484763304",
                fileName: "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad"
            ) {
                success
                url
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["downloadEventFile"]
    assert "url" in result["data"]["downloadEventFile"]


@pytest.mark.changes_db
async def test_remove_event_evidence() -> None:
    """Check for removeEventEvidence mutation."""
    query = """
        mutation {
            removeEventEvidence(eventId: "484763304",
                                evidenceType: FILE) {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["removeEventEvidence"]
