# Standard library
import json
from glob import (
    iglob,
)
from itertools import (
    chain,
)
import os
from typing import (
    Dict,
    Iterator,
)

# Third party libraries
import pytest

# Local libraries
from integrates.graphql import (
    create_session,
    end_session,
)
from parse_cfn.loader import (
    load_as_yaml_without_line_number,
)


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_branch() -> Iterator[str]:
    yield os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_group(test_branch: str) -> Iterator[str]:
    mapping: Dict[str, str] = {
        'drestrepoatfluid': 'wausau',
        'kamadoatfluid': 'worcester',
        'master': 'tovuz',
    } if os.environ.get('CI') else {
        'drestrepoatfluid': 'djibo',
        'kamadoatfluid': 'magdalena',
    }

    yield mapping.get(test_branch, 'utuado')


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')  # type: ignore
def test_integrates_session(test_integrates_api_token: str) -> Iterator[None]:
    token = create_session(api_token=test_integrates_api_token)
    try:
        yield
    finally:
        end_session(token)


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_prepare_cfn_json_data() -> None:
    for path in chain(
        iglob('test/data/lib_path/**/*.yaml', recursive=True),
        iglob('test/data/parse_cfn/**/*.yaml', recursive=True),
    ):
        # Take the yaml and dump it as json as is
        with open(path) as source, open(path + '.json', 'w') as target:
            source_data = load_as_yaml_without_line_number(source.read())
            target.write(json.dumps(source_data, indent=2))
