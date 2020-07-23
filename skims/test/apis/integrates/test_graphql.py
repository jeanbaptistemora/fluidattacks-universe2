# Local libraries
from apis.integrates.graphql import (
    Session,
)

# Third party libraries
import pytest


@pytest.mark.asyncio  # type: ignore
async def test_session() -> None:
    assert Session.value is not None
