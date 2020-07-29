# Local libraries
import sys
from typing import List

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
    type=click.Choice(['generic', 'product', 'services']),
    default='generic'
)
def flavor_management(flavor_name: str) -> None:
    success: bool = True
    regex_mr_title: str = r'^(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$'
    fail_tests: List[str] = []
    warn_tests: List[str] = []
    if 'generic' in flavor_name:
        fail_tests = [
            'mr_under_max_deltas',
            'all_pipelines_successful',
            'mr_message',
            'branch_equals_to_user',
            'most_relevant_type',
            'commits_user',
            'mr_user',
        ]
        warn_tests = [
            'one_commit_per_mr',
            'close_issue_directive',
        ]
    elif 'product' in flavor_name:
        regex_mr_title = r'^(?:all|forces|integrates|reviews|skims|sorts)' \
                         r'\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$'
        fail_tests = [
            'mr_under_max_deltas',
            'all_pipelines_successful',
            'mr_message',
            'branch_equals_to_user',
            'most_relevant_type',
            'commits_user',
            'mr_user',
        ]
        warn_tests = [
            'one_commit_per_mr',
            'close_issue_directive',
        ]
    elif 'services' in flavor_name:
        fail_tests = [
            'mr_under_max_deltas',
            'all_pipelines_successful',
            'branch_equals_to_user',
            'commits_user',
            'mr_user',
            'one_commit_per_mr',
        ]
        warn_tests = [
            'close_issue_directive',
        ]
    success = run_flavor(fail_tests, warn_tests, regex_mr_title)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    entrypoint()
