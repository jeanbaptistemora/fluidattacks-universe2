import asyncio
import logging
import pytest

import authz
from settings import LOGGING


logging.config.dictConfig(LOGGING)


@pytest.fixture(autouse=True, scope="session")
async def load_enforcers(request):
    """Load policies from DB into the enforcers."""
    await authz.grant_user_level_role("unittest", "admin")


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
