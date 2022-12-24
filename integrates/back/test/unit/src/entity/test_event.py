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
    Optional,
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
    filename = os.path.join(filename, "./mock/evidences/test-anim.webm")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-zxcvbnm105.webm", test_file, "video/webm"
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
        == "unittesting_540462628_evidence_image_1.webm"
    )
    assert result["data"]["event"]["evidenceDate"].split(" ")[0] == (
        today.split("T")[0]
    )
