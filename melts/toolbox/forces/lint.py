# Standard library
import ast
from glob import glob

# Third party libraries
import pykwalify.core
import pykwalify.errors
import ruamel.yaml as yaml

# Local libraries
from toolbox import (
    logger,
    utils,
)
from toolbox.utils.function import shield


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
    logger.info(f'Running prospector over: {exploit_path}')

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
    logger.info(f'Running linter for add_finding over: {exploit_path}')

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

    if add_findings > 0:
        logger.error('Exploits must not have add_finding')
        logger.error()
        return False

    return True


def _one_exploit_by_path_for_reason(exploit_path: str) -> bool:
    logger.info(f'Running linter for exploit reason: {exploit_path}')

    success: bool = True
    schema_path: str = 'forces/config/schemas/.reason.yaml'

    try:
        with open(exploit_path) as exploit_handle:
            pykwalify.core.Core(
                source_data=yaml.safe_load(exploit_handle),
                schema_files=[
                    schema_path,
                ],
            ).validate(raise_exception=True)
    except (pykwalify.errors.SchemaError, yaml.error.YAMLError) as exc:
        logger.error(f'{exploit_path} must match schema')
        logger.info()
        logger.info(f'The schema can be found at: {schema_path}')
        logger.info(f'The problem was: {exc}')
        success = False

    return success


@shield()
def one_exploit_by_path(exploit_path: str) -> bool:
    """Run all linters available over one exploit."""
    if '.reason' in exploit_path:
        return _one_exploit_by_path_for_reason(exploit_path)

    return _one_exploit_by_path_with_prospector(exploit_path) \
        and _one_exploit_by_path_with_mypy(exploit_path) \
        and _one_exploit_by_path_for_deprecated_methods(exploit_path)


@shield()
def many_exploits_by_subs_and_filter(subs: str, filter_str: str) -> bool:
    """Run all linters available over many exploits."""
    filter_str = filter_str or ''
    pattern_exp = f'groups/{subs}/forces/*/exploits/*.exp'

    return all(
        one_exploit_by_path(exploit_path)
        for exploit_path in sorted(glob(pattern_exp))
        if filter_str in exploit_path
    )


@shield()
def many_exploits_by_change_request(ref: str = 'HEAD') -> bool:
    """Run all linters available over the current change request."""
    changed_exploits = \
        utils.generic.get_change_request_touched_and_existing_exploits(ref)

    return all(
        one_exploit_by_path(exploit_path)
        for exploit_path in changed_exploits
    )


@shield()
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
