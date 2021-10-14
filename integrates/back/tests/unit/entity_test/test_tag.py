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
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_tag_query() -> None:
    """Check for group alert."""
    query = """
        query{
            tag(tag: "test-groups"){
                lastClosedVulnerability
                maxOpenSeverity
                maxSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                meanRemediate
                name
                groups {
                    closedVulnerabilities
                    name
                    openVulnerabilities
                }
                __typename
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session("integratesuser@gmail.com")
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "groups" in result["data"]["tag"]
    assert result["data"]["tag"]["lastClosedVulnerability"] == 50
    assert result["data"]["tag"]["meanRemediateLowSeverity"] == 116
    assert result["data"]["tag"]["meanRemediateMediumSeverity"] == 135.9
    assert result["data"]["tag"]["meanRemediate"] == 123
    assert result["data"]["tag"]["maxOpenSeverity"] == 3.3
    assert result["data"]["tag"]["maxSeverity"] == 4.3


async def test_get_tag_query_access_denied() -> None:
    query = """
        query{
            tag(tag: "another-tag"){
                lastClosedVulnerability
                maxOpenSeverity
                meanRemediate
                name
                groups {
                    closedVulnerabilities
                    name
                    openVulnerabilities
                }
                __typename
            }
        }
    """
    data = {"query": query}

    request = await create_dummy_session("unittests")
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied or tag not found"
