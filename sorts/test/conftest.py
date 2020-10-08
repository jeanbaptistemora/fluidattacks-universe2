# Standard libraries
import os
from typing import Iterator

# Third-party libraries
import pytest

# Local libraries
from integrates.graphql import (
    create_session,
    end_session,
)


@pytest.fixture(autouse=True, scope='session')
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')
def test_integrates_session(test_integrates_api_token: str) -> Iterator[None]:
    token = create_session(api_token=test_integrates_api_token)
    try:
        yield
    finally:
        end_session(token)
