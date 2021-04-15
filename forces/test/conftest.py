# Standard library
import os
from typing import (
    Iterator,
)

# Third party libraries
import pytest


@pytest.fixture(scope='session')
def test_group() -> Iterator[str]:
    yield 'herrin'


@pytest.fixture(scope='session')
def test_finding() -> Iterator[str]:
    yield '940350540'


@pytest.fixture(scope='session')
def test_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_FORCES_API_TOKEN']


@pytest.fixture(scope='session')
def test_endpoint() -> Iterator[str]:
    yield 'https://app.fluidattacks.com/api'
