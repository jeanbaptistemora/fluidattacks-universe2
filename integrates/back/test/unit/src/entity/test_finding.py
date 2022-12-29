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
from freezegun import (
    freeze_time,
)
from groups.domain import (
    get_open_vulnerabilities,
)
import pytest
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


@freeze_time("2020-12-01")
async def test_finding_age() -> None:
    """Check for finding age."""
    query = """{
      finding(identifier: "422286126"){
          age
          lastVulnerability
          openAge
          minTimeToRemediate
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["finding"]["age"] == 332
    assert result["data"]["finding"]["lastVulnerability"] == 332
    assert result["data"]["finding"]["openAge"] == 332
    assert result["data"]["finding"]["minTimeToRemediate"] == 18


@pytest.mark.changes_db
async def test_filter_deleted_findings() -> None:
    """Check if vulns of removed findings are filtered out"""
    finding_id = "988493279"
    group_name = "unittesting"
    mutation = f"""
      mutation {{
        removeFinding(
          findingId: "{finding_id}", justification: NOT_REQUIRED
        ) {{
          success
        }}
      }}
    """
    loaders: Dataloaders = get_new_context()
    open_vulns = await get_open_vulnerabilities(loaders, group_name)

    data = {"query": mutation}
    result = await _get_result(data, loaders=loaders)
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]
    loaders = get_new_context()
    assert await get_open_vulnerabilities(loaders, group_name) < open_vulns
