# Standard library
import asyncio
import os
from typing import (
    AsyncIterator,
    Iterator,
)

# Third party libraries
import pytest

# Local libraries
from apis.integrates.graphql import (
    create_session,
)
from apis.integrates.domain import (
    delete_closest_findings,
)


@pytest.fixture(scope='session', autouse=True)  # type: ignore
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    yield loop


@pytest.fixture(scope='session', autouse=True)  # type: ignore
async def test_finding_title(
    test_group: str,
    test_integrates_session: None,
) -> AsyncIterator[str]:
    title: str = 'F.S.0. test finding, please delete'

    await delete_closest_findings(
        group=test_group,
        title=title,
    )

    yield title


@pytest.fixture(scope='session')  # type: ignore
def test_group() -> Iterator[str]:
    yield 'worcester'


@pytest.fixture(scope='session')  # type: ignore
def test_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='session', autouse=True)  # type: ignore
def test_integrates_session(test_token: str) -> Iterator[None]:
    create_session(api_token=test_token)
    yield
