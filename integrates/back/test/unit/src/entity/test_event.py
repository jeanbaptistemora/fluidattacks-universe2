# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from newutils import (
    datetime as datetime_utils,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

pytestmark = pytest.mark.asyncio


async def _get_result(
    data: Dict[str, Any],
    user: str = "integratesmanager@gmail.com",
    loaders: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=user)
    request = apply_context_attrs(
        request, loaders or get_new_context()  # type: ignore
    )
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result


async def test_events() -> None:
    """Check for events."""
    query = """{
        events(groupName: "unittesting"){
            groupName
            detail
        }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "events" in result["data"]
    assert result["data"]["events"][0]["groupName"] == "unittesting"
    assert len(result["data"]["events"][0]["detail"]) >= 1


@pytest.mark.changes_db
async def test_solve_event() -> None:
    """Check for solveEvent mutation."""
    loaders: Dataloaders = get_new_context()
    # The event with this ID starts with a couple of reattacks on hold
    reattacks_on_hold: Tuple[
        Vulnerability, ...
    ] = await loaders.event_vulnerabilities_loader.load("418900971")
    for reattack in reattacks_on_hold:
        assert (
            reattack.verification.status  # type: ignore
            == VulnerabilityVerificationStatus.ON_HOLD
        )

    query = """
        mutation {
            solveEvent(
                eventId: "418900971"
                reason: OTHER
                other: "Test"
            ) {
                success
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    if "errors" not in result:
        assert "errors" not in result
        assert "success" in result["data"]["solveEvent"]
        # Solving an Event puts any reattack on hold back to requested
        reattacks_requested: List[Vulnerability] = [
            await loaders.vulnerability.load(reattack.id)
            for reattack in reattacks_on_hold
        ]
        for reattack in reattacks_requested:
            assert (
                reattack.verification.status  # type: ignore
                == VulnerabilityVerificationStatus.REQUESTED
            )
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
                            parentComment: "0",
                            content: "Test comment") {
                success
                commentId
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
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
    filename = os.path.join(filename, "./mock/evidences/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-zxcvbnm105.gif", test_file, "image/gif"
        )
        variables = {
            "eventId": "540462628",
            "evidenceType": "IMAGE_1",
            "file": uploaded_file,
        }
        data = {"query": query, "variables": variables}
        result = await _get_result(data)

    assert "errors" not in result
    assert "success" in result["data"]["updateEventEvidence"]

    today = datetime_utils.get_iso_date()
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
    result = await _get_result(data)
    assert "errors" not in result
    assert (
        result["data"]["event"]["evidence"]
        == "unittesting_540462628_evidence_image_1.gif"
    )
    assert result["data"]["event"]["evidenceDate"].split(" ")[0] == (
        today.split("T")[0]
    )


@pytest.mark.changes_db
async def test_download_event_file() -> None:
    """Check for downloadEventFile mutation."""
    query = """
        mutation {
            downloadEventFile(
                eventId: "484763304",
                fileName: "unittesting_484763304_evidence_file_1.csv"
            ) {
                success
                url
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["downloadEventFile"]
    assert "url" in result["data"]["downloadEventFile"]


@pytest.mark.changes_db
async def test_remove_event_evidence() -> None:
    """Check for removeEventEvidence mutation."""
    query = """
        mutation {
            removeEventEvidence(eventId: "484763304",
                                evidenceType: FILE_1) {
                success
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeEventEvidence"]
