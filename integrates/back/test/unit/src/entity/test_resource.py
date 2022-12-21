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
import json
import os
import pytest
from typing import (
    Any,
    Dict,
    Optional,
)

pytestmark = pytest.mark.asyncio


async def _get_result(
    data: Dict[str, Any], context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(  # type: ignore
        request,  # type: ignore
        loaders=context if context else get_new_context(),
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


@pytest.mark.changes_db
async def test_add_files() -> None:
    """Check for SignPostUrlMutation mutation."""
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/evidences/test-anim.gif")
    with open(filename, "rb") as test_file:
        file_data = [
            {
                "description": "test",
                "fileName": test_file.name.split("/")[2],
                "uploadDate": "",
            }
        ]
        query = """
            mutation SignPostUrlMutation(
                $filesData: JSONString!, $groupName: String!
            ) {
                signPostUrl (
                    filesData: $filesData,
                    groupName: $groupName) {
                        success
                }
            }
        """
        variables = {
            "filesData": json.dumps(file_data),
            "groupName": "UNITTESTING",
        }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    if "errors" not in result:
        assert "errors" not in result
        assert "success" in result["data"]["signPostUrl"]
        assert result["data"]["signPostUrl"]["success"]
    else:
        pytest.skip("Expected error")
