# Local libraries
import sys
from typing import List, Dict

# Third party libraries
import click

# Local libraries
from core.flavors import (
    run_flavor
)


@click.group(name='entrypoint')
def entrypoint() -> None:
    """Main comand line group."""


@entrypoint.command(
    'flavor',
)
@click.argument(
    'flavor_name',
    type=click.Choice(['generic', 'product', 'services', 'challenges']),
    default='generic'
)
def flavor_management(flavor_name: str) -> None:
    success: bool = True
    regex_mr_title: str = r'^(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$'
    relevances: Dict[str, int] = {
        'rever': 1,
        'feat': 2,
        'perf': 3,
        'fix': 4,
        'refac': 5,
        'test': 6,
        'style': 7,
    }
    fail_tests: List[str] = [
        'mr_under_max_deltas',
        'all_pipelines_successful',
        'branch_equals_to_user',
        'commits_user',
        'mr_user',
    ]
    warn_tests: List[str] = [
        'close_issue_directive',
    ]
    if 'generic' in flavor_name:
        fail_tests.extend((
            'mr_message',
        ))
        warn_tests.extend((
            'one_commit_per_mr',
        ))
    elif 'product' in flavor_name:
        regex_mr_title = r'^(?:all|forces|integrates|reviews|skims|sorts)' \
                         r'\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$'
        fail_tests.extend((
            'mr_message',
            'most_relevant_type',
        ))
        warn_tests.extend((
            'one_commit_per_mr',
        ))
    elif 'services' in flavor_name:
        fail_tests.extend((
            'one_commit_per_mr',
        ))
    elif 'challenges' in flavor_name:
        regex_mr_title = r'^(\w*)\((\w*)\):\s(#\d+)(.\d+)?\s(.*)$'
        relevances['sol'] = 8
        fail_tests.extend((
            'mr_message',
            'most_relevant_type',
        ))
        warn_tests.extend((
            'one_commit_per_mr',
        ))
    success = run_flavor(fail_tests, warn_tests, regex_mr_title, relevances)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    entrypoint()
