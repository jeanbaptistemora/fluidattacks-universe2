import asyncio
import authz
import logging
import pytest
from settings import (
    LOGGING,
)
from typing import (
    Any,
    AsyncGenerator,
)

logging.config.dictConfig(LOGGING)  # type: ignore


@pytest.fixture(autouse=True, scope="session")
async def load_enforcers() -> None:
    """Load policies from DB into the enforcers."""
    await authz.grant_user_level_role("unittest", "admin")


@pytest.fixture(autouse=True)
def disable_logging() -> None:
    """Disable logging in all tests."""
    logging.disable(logging.INFO)


@pytest.yield_fixture(scope="session")
def event_loop() -> AsyncGenerator[Any, None]:  # type: ignore
    loop = asyncio.get_event_loop_policy().new_event_loop()
    # Exception: WF(AsyncGenerator is subtype of iterator)
    yield loop  # NOSONAR
    loop.close()
