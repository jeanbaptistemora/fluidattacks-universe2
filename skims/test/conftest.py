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
    Any,
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
from utils.ctx import (
    create_test_context,
)

# Constants
TEST_GROUPS = {
    'benchmark_cmdi',
    'benchmark_pathtraver',
    'benchmark_securecookie',
    'benchmark_weakrand',
    'functional',
    'unittesting',
}

# Side effects
os.chdir('..')
create_test_context(debug=False)


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        '--skims-test-group',
        action='store',
        metavar='SKIMS_TEST_GROUP',
    )


def pytest_runtest_setup(item: Any) -> None:
    # We pass this command line option to tell what group do we want to run
    # This split the big test suite in components
    skims_test_group = item.config.getoption('--skims-test-group')

    # Validate that the dev specified a group that is run on the CI
    if not skims_test_group:
        raise ValueError('skims-test-group not specified')
    if skims_test_group != 'all' and skims_test_group not in TEST_GROUPS:
        raise ValueError(
            f'skims-test-group must be one of: {TEST_GROUPS}, or all',
        )

    # The test expects to run on one of these groups
    # If the dev forgets to specify it while writing the test it'll run
    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name='skims_test_group')
    }

    # Validate that the dev specified a group that is run on the CI
    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f'skims-test-group must be one of: {TEST_GROUPS}')

    # Small logic to skip tests that should not run
    if runnable_groups:
        if skims_test_group == 'all' or skims_test_group in runnable_groups:
            # Test should execute
            pass
        else:
            pytest.skip(f'Requires skims test group in: {runnable_groups}')


@pytest.fixture(autouse=True, scope='session')
def test_branch() -> Iterator[str]:
    yield os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')
def test_group(
    test_branch: str,  # pylint: disable=redefined-outer-name
) -> Iterator[str]:
    # Create 2 groups on Integrates and assign them to your branch
    mapping: Dict[str, str] = {
        'kamadoatfluid': 'worcester',
        'master': 'wausau',
        'drestrepoatfluid': 'tacna',
    } if os.environ.get('CI') else {
        'kamadoatfluid': 'magdalena',
        'drestrepoatfluid': 'jessup',
        'master': 'djibo',
    }

    yield mapping[test_branch]


@pytest.fixture(autouse=True, scope='session')
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')
def test_integrates_session(
    test_integrates_api_token: str,  # pylint: disable=redefined-outer-name
) -> Iterator[None]:
    token = create_session(api_token=test_integrates_api_token)
    try:
        yield
    finally:
        end_session(token)


@pytest.fixture(autouse=True, scope='session')
def test_prepare_cfn_json_data() -> None:
    for path in chain(
        iglob('skims/test/data/lib_path/**/*.yaml', recursive=True),
        iglob('skims/test/data/parse_cfn/**/*.yaml', recursive=True),
    ):
        # Take the yaml and dump it as json as is
        with open(path) as source, open(path + '.json', 'w') as target:
            source_data = load_as_yaml_without_line_number(source.read())
            target.write(json.dumps(source_data, indent=2))
