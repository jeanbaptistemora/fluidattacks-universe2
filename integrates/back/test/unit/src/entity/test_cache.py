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
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_invalidate_cache() -> None:
    """Check for invalidate_cache mutation."""
    query = """
        mutation {
            invalidateCache(pattern: "unittest") {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["invalidateCache"]
