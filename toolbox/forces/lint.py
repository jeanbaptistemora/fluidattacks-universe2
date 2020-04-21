# Standard library
import ast
from glob import glob

# Third party libraries

# Local libraries
from toolbox import (
    logger,
    utils,
)


def _one_exploit_by_path_with_mypy(exploit_path: str) -> bool:
    logger.info(f'Running static checker over: {exploit_path}')
    status, stdout, stderr = utils.generic.run_command(
        cmd=['mypy', '--ignore-missing-imports', exploit_path],
        cwd='.',
        env={})

    if status:
        logger.error('Static checker has failed, output:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False

    return True


def _one_exploit_by_path_with_prospector(exploit_path: str) -> bool:
    logger.info(f'Running linter over: {exploit_path}')
    status, stdout, stderr = utils.generic.run_command(
        cmd=[
            'prospector',
            '--output-format', 'vscode',
            '--messages-only',
            '--profile', 'break-build/config/prospector/exploits.yml',
            exploit_path,
        ],
        cwd='.',
        env={})

    if status:
        logger.error('Prospector has failed, output:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False

    return True


def _one_exploit_by_path_for_deprecated_methods(exploit_path: str) -> bool:
    logger.info(f'Running linter for exploit title over: {exploit_path}')

    if '.cannot' in exploit_path:
        return True

    calls = list()
    with open(exploit_path) as exploit_handle:
        exploit_content: str = exploit_handle.read()

        for node in ast.walk(ast.parse(exploit_content)):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)

    add_findings: int = \
        sum('add_finding' in call for call in calls)

    generic_static_exploits: int = \
        sum('generic_static_exploit' in call for call in calls)

    if add_findings + generic_static_exploits > 1:
        logger.error('Exploits must have 1 (and only 1) add_finding')
        logger.error()
        logger.info('The following functions are allowed:')
        logger.info('- generic.add_finding')
        logger.info('- utilities.generic_static_exploit')
        logger.info()
        return False

    return True


def one_exploit_by_path(exploit_path: str) -> bool:
    """Run all linters available over one exploit."""
    return _one_exploit_by_path_with_prospector(exploit_path) \
        and _one_exploit_by_path_with_mypy(exploit_path) \
        and _one_exploit_by_path_for_deprecated_methods(exploit_path)


def many_exploits_by_subs_and_filter(subs: str, filter_str: str) -> bool:
    """Run all linters available over many exploits."""
    filter_str = filter_str or ''
    glob_pattern = f'subscriptions/{subs}/break-build/*/exploits/*.exp'

    return all(
        one_exploit_by_path(exploit_path)
        for exploit_path in sorted(glob(glob_pattern))
        if filter_str in exploit_path
    )


def many_exploits_by_change_request(ref: str = 'HEAD') -> bool:
    """Run all linters available over the current change request."""
    changed_exploits = \
        utils.generic.get_change_request_touched_and_existing_exploits(ref)

    return all(
        one_exploit_by_path(exploit_path)
        for exploit_path in changed_exploits
    )
