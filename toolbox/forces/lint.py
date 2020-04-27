# Standard library
import ast
from glob import glob
from typing import (
    Tuple,
)

# Third party libraries

# Local libraries
from toolbox import (
    constants,
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
            '--profile', 'forces/config/prospector/exploits.yml',
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

    if add_findings + generic_static_exploits != 1:
        logger.error('Exploits must have 1 (and only 1) add_finding')
        logger.error()
        logger.info('The following functions are allowed:')
        logger.info('- generic.add_finding')
        logger.info('- utilities.generic_static_exploit')
        logger.info()
        return False

    return True


def _one_exploit_by_path_for_reason(exploit_path: str) -> bool:
    success: bool = True
    valid_reasons: Tuple[str, ...] = (
        'ASSERTS CAPABILITIES',
        'AVAILABILITY CONCERNS',
        'REQUIRED HUMAN INTERACTION',
        'UNREACHABLE ENVIRONMENT',
        'OTHER',
    )

    if '.cannot' in exploit_path:
        with open(exploit_path) as handle:
            exploit_content = handle.read()

        regex = constants.RE_EXPLOIT_REASON
        regex_match = regex.search(exploit_content)
        if regex_match:
            reason = regex_match.groupdict().get('reason', '')
            if reason in valid_reasons:
                success = True
            else:
                success = False
                logger.error(f"Invalid reason: {reason}")
                logger.info(f'Valid exploit reasons are:')
                for reason in valid_reasons:
                    logger.info(f'- {reason}')
        else:
            success = False
            logger.error(f'Exploit reasons must match: {regex}')
            logger.info()
            logger.info('Example:')
            logger.info()
            logger.info(
                f'# Not possible exploit due to: UNREACHABLE ENVIRONMENT')
            logger.info()
    else:
        success = True

    return success


def one_exploit_by_path(exploit_path: str) -> bool:
    """Run all linters available over one exploit."""
    return _one_exploit_by_path_with_prospector(exploit_path) \
        and _one_exploit_by_path_with_mypy(exploit_path) \
        and _one_exploit_by_path_for_deprecated_methods(exploit_path) \
        and _one_exploit_by_path_for_reason(exploit_path)


def many_exploits_by_subs_and_filter(subs: str, filter_str: str) -> bool:
    """Run all linters available over many exploits."""
    filter_str = filter_str or ''
    glob_pattern = f'subscriptions/{subs}/forces/*/exploits/*.exp'

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


def check_folder_content():
    """Verify that drills do not contain forces code."""
    path_patterns = (r'\w+\/forces\/\w+\/((.mailmap)|(toe)|(config)'
                     r'|(\w+.(yaml|yml|csv|adoc)))')

    files = list(utils.generic.glob_re(path_patterns, 'inactive'))
    if files:
        logger.error(('The forces folder must not contain drill code, please'
                      ' relocate the following files'))
        for path in files:
            logger.info(f'    {path}')
        return False

    return True
