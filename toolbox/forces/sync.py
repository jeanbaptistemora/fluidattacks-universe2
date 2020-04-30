# Standard library
import difflib
import glob
import json
import operator
import os
import textwrap
from datetime import datetime
from typing import (
    Dict,
    List,
    Set,
    Tuple,
)
# Third party libraries

# Local libraries
from toolbox import (
    api,
    constants,
    logger,
    utils,
)


def _get_asserts_msg(
    *,
    num_error_asserts: int,
    num_open_asserts: int,
    num_unknown_asserts: int,
) -> str:
    # Error if at least one error
    # Open if at least one open and no errors
    # Unknown if at least one unknown, no errors and no opens
    # Closed if no errors or opens or unknowns
    return {
        num_unknown_asserts > 0: 'UNKNOWN',
        num_open_asserts > 0: 'OPEN',
        num_error_asserts > 0: 'ERROR',
    }.get(True, 'CLOSED')


def _get_integrates_msg(
    *,
    num_open_integrates: int,
) -> str:
    # Open if at least one is open
    return 'OPEN' if num_open_integrates > 0 else 'CLOSED'


def _get_bb_fernet_key(subscription: str) -> str:
    return utils.generic.get_sops_secret(
        f'forces_aws_secret_access_key',
        f'subscriptions/{subscription}/config/secrets.yaml',
        f'continuous-{subscription}')


def _get_bb_aws_role_arns(subs: str) -> Tuple[str, ...]:
    config_path = (
        f'subscriptions/{subs}'
        f'/forces/dynamic/resources/BB_AWS_ROLE_ARNS.list'
    )

    if os.path.exists(config_path):
        with open(config_path) as config_handle:
            return tuple(
                filter(operator.truth,
                       map(operator.methodcaller('strip'),
                           config_handle.readlines())))

    return tuple()


def _get_bb_resources(subs: str, kind: str) -> str:
    return \
        os.path.abspath(f'subscriptions/{subs}/forces/{kind}/resources')


def _get_patch_file_name(subs: str) -> str:
    return f'check-sync-results.{subs}.patch'


def _is_synced(
    *,
    num_error_asserts: int,
    num_open_asserts: int,
    num_open_integrates: int,
) -> bool:
    return num_error_asserts == 0 \
        and num_open_asserts == num_open_integrates


def _diff_vulnerabilities(
    subs: str,
    exploit_ref: str,
    integrates_ref: str,
    exploit: Tuple[api.asserts.Vulnerability, ...],
    integrates: List[Dict[str, str]],
):
    exploit_open = tuple(sorted(set(
        f'{vul.what} @ {vul.where}\n'
        for vul in exploit
        if vul.status == 'OPEN'
    )))

    integrates_open = tuple(sorted(set(
        f"{vul['full_path']} @ {vul['specific']}\n"
        for vul in integrates
        if vul['status'] == 'OPEN'
    )))

    diff = difflib.unified_diff(
        exploit_open,
        integrates_open,
        fromfile=exploit_ref,
        tofile=integrates_ref
    )

    patch_file_name = _get_patch_file_name(subs)
    with open(patch_file_name, 'a') as patch_file_handle:
        patch_file_handle.writelines(diff)
        patch_file_handle.write('\n')


def _print_results_summary(results: List[dict]):
    num_tests = len(results)
    num_synced = sum(result['is_synced'] for result in results)
    num_not_synced = num_tests - num_synced
    exploits = 'exploit' if num_tests == 1 else 'exploits'

    if num_tests == num_synced:
        logger.info(f'Summary: {num_tests} {exploits} tested, all ok!')
    else:
        logger.info(
            f'Summary: {num_tests} {exploits} tested'
            f', {num_synced} synced'
            f', {num_not_synced} not synced')


def _run_static_exploit(
    *,
    exploit_path: str,
    exploit_output_path: str,
    repository_path: str,
    bb_fernet_key: str,
    bb_resources: str,
) -> Tuple[int, str, str]:
    """Run a static exploit and return it's exit_code, stdout and stderr."""
    repo: str = os.path.basename(repository_path)

    cmd: str = f"""
        echo '---' >> '{exploit_output_path}'
        echo 'repository: {repo}' >> '{exploit_output_path}'
        asserts -eec -n -ms '{exploit_path}' > '{exploit_output_path}_'
        exit_code=$?
        cat '{exploit_output_path}_'
        cat '{exploit_output_path}_' >> '{exploit_output_path}'
        rm -f '{exploit_output_path}_' >  /dev/null
        exit ${{exit_code}}
        """

    cmd = ';'.join(textwrap.dedent(cmd)[1:-1].splitlines())

    env: Dict[str, str] = {
        'FA_NOTRACK': 'true',
        'FA_STRICT': 'true',
        'BB_FERNET_KEY': bb_fernet_key,
        'BB_RESOURCES': bb_resources,
        'CURRENT_EXPLOIT_KIND': 'static'
    }

    return utils.generic.run_command_old(cmd=cmd, cwd=repository_path, env=env)


def _run_dynamic_exploit(
    *,
    exploit_path: str,
    exploit_output_path: str,
    subs_path: str,
    bb_aws_role_arns: Tuple[str, ...],
    bb_fernet_key: str,
    bb_resources: str,
) -> Tuple[int, str, str]:
    """Run a dynamic exploit and return it's exit_code, stdout and stderr."""
    cmd: str = f"""
        asserts -eec -n -ms '{exploit_path}' > '{exploit_output_path}_'
        exit_code=$?
        cat '{exploit_output_path}_'
        cat '{exploit_output_path}_' >> '{exploit_output_path}'
        rm -f '{exploit_output_path}_' >  /dev/null
        exit ${{exit_code}}
        """

    cmd = ';'.join(textwrap.dedent(cmd)[1:-1].splitlines())

    env: Dict[str, str] = {
        'BB_AWS_ROLE_ARNS': ','.join(bb_aws_role_arns),
        'BB_FERNET_KEY': bb_fernet_key,
        'BB_RESOURCES': bb_resources,
        'CURRENT_EXPLOIT_KIND': 'dynamic',
        'FA_NOTRACK': 'true',
        'FA_STRICT': 'true',
    }

    return utils.generic.run_command_old(cmd=cmd, cwd=subs_path, env=env)


def _validate_one_static_exploit(
    *,
    bb_fernet_key: str,
    bb_resources: str,
    exploit_output_path: str,
    exploit_path: str,
    finding_id: str,
    subs: str,
) -> List[dict]:
    """Validate Synchronization in one static exploit and return results."""
    results: List[dict] = []

    if os.path.isfile(exploit_output_path):
        os.remove(exploit_output_path)

    integrates_repositories_data = \
        utils.integrates.get_finding_static_data(finding_id)
    integrates_repositories_vulns = \
        utils.integrates.get_finding_static_repos_vulns(finding_id)

    repositories_local: Set[str] = {
        repository
        for repository in os.listdir(f'subscriptions/{subs}/fusion')
        if os.path.isdir(f'subscriptions/{subs}/fusion/{repository}')
    }

    repositories_integrates: Set[str] = \
        set(integrates_repositories_data.keys())

    for repo in repositories_integrates.union(repositories_local):
        repository_path: str = f'subscriptions/{subs}/fusion/{repo}'

        if not os.path.isdir(repository_path):
            # This repo exist on Integrates and not locally, we cannot test
            continue

        _, asserts_stdout, _ = _run_static_exploit(
            exploit_path=exploit_path,
            exploit_output_path=exploit_output_path,
            repository_path=repository_path,
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources)

        integrates_vulns = \
            integrates_repositories_data.get(repo, [])
        num_open_integrates = \
            integrates_repositories_vulns.get(repo, {}).get('open', 0)
        num_closed_integrates = \
            integrates_repositories_vulns.get(repo, {}).get('closed', 0)

        asserts_vulns = tuple(
            api.asserts.iterate_vulnerabilities_from_content(
                asserts_stdout, repo))
        num_open_asserts = \
            sum(vul.status.startswith('OPEN') for vul in asserts_vulns)
        num_unknown_asserts = \
            sum(vul.status.startswith('UNKNOWN') for vul in asserts_vulns)
        num_error_asserts = \
            sum(vul.status.startswith('ERROR') for vul in asserts_vulns)

        # Open if at least one vuln is open
        amsg = _get_asserts_msg(
            num_error_asserts=num_error_asserts,
            num_open_asserts=num_open_asserts,
            num_unknown_asserts=num_unknown_asserts,
        )
        imsg = _get_integrates_msg(
            num_open_integrates=num_open_integrates,
        )

        # The synced equation
        is_synced = _is_synced(
            num_error_asserts=num_error_asserts,
            num_open_asserts=num_open_asserts,
            num_open_integrates=num_open_integrates,
        )

        if not is_synced:
            logger.info(
                f'  {finding_id:<10}: {repo:<60} '
                f'{imsg!s:<6} I ('
                f'{num_open_integrates!s:<3} o, '
                f'{num_closed_integrates!s:<3} c), '
                f'{amsg!s:<7} E ('
                f'{num_error_asserts!s:<3} e, '
                f'{num_open_asserts!s:<3} o, '
                f'{num_unknown_asserts!s:<3} u)'
            )
            _diff_vulnerabilities(
                subs,
                exploit_output_path,
                utils.integrates.get_integrates_url(subs, finding_id),
                asserts_vulns,
                integrates_vulns)

        results.append(dict(
            num_error_asserts=num_error_asserts,
            num_open_asserts=num_open_asserts,
            num_unknown_asserts=num_unknown_asserts,
            num_open_integrates=num_open_integrates,
            num_closed_integrates=num_closed_integrates,
            repository=repo,
        ))

    summary: dict = dict(
        exploit_path=os.path.relpath(exploit_path),
        exploit_type='static',
        **{
            key: sum(result[key] for result in results)
            for key in (
                'num_error_asserts',
                'num_open_asserts',
                'num_unknown_asserts',
                'num_open_integrates',
                'num_closed_integrates',
            )
        },
    )
    summary['result_asserts'] = _get_asserts_msg(
        num_error_asserts=summary['num_error_asserts'],
        num_open_asserts=summary['num_open_asserts'],
        num_unknown_asserts=summary['num_unknown_asserts'],
    )
    summary['result_integrates'] = _get_integrates_msg(
        num_open_integrates=summary['num_open_integrates'],
    )
    summary['is_synced'] = _is_synced(
        num_error_asserts=summary['num_error_asserts'],
        num_open_asserts=summary['num_open_asserts'],
        num_open_integrates=summary['num_open_integrates'],
    )

    return [summary]


def _validate_one_dynamic_exploit(
    *,
    bb_aws_role_arns: Tuple[str, ...],
    bb_fernet_key: str,
    bb_resources: str,
    exploit_output_path: str,
    exploit_path: str,
    finding_id: str,
    subs: str,
) -> List[dict]:
    """Validate Synchronization in one static exploit and return results."""
    if os.path.isfile(exploit_output_path):
        os.remove(exploit_output_path)

    integrates_vulns = \
        utils.integrates.get_finding_dynamic_states(finding_id)
    num_open_integrates = \
        sum(1 for _, _, is_open in integrates_vulns if is_open)
    num_closed_integrates = \
        sum(1 for _, _, is_open in integrates_vulns if not is_open)

    _, asserts_stdout, _ = _run_dynamic_exploit(
        exploit_path=exploit_path,
        exploit_output_path=exploit_output_path,
        subs_path=f'subscriptions/{subs}',
        bb_aws_role_arns=bb_aws_role_arns,
        bb_fernet_key=bb_fernet_key,
        bb_resources=bb_resources)

    asserts_vulns = tuple(
        api.asserts.iterate_vulnerabilities_from_content(asserts_stdout))
    num_open_asserts = \
        sum(vul.status.startswith('OPEN') for vul in asserts_vulns)
    num_unknown_asserts = \
        sum(vul.status.startswith('UNKNOWN') for vul in asserts_vulns)
    num_error_asserts = \
        sum(vul.status.startswith('ERROR') for vul in asserts_vulns)

    amsg = _get_asserts_msg(
        num_error_asserts=num_error_asserts,
        num_open_asserts=num_open_asserts,
        num_unknown_asserts=num_unknown_asserts,
    )
    imsg = _get_integrates_msg(
        num_open_integrates=num_open_integrates,
    )

    # The synced equation
    is_synced = _is_synced(
        num_error_asserts=num_error_asserts,
        num_open_asserts=num_open_asserts,
        num_open_integrates=num_open_integrates,
    )

    if not is_synced:
        logger.info(
            f'  {finding_id:<10}: {str():<60} '
            f'{imsg!s:<6} I ('
            f'{num_open_integrates!s:<3} o, '
            f'{num_closed_integrates!s:<3} c), '
            f'{amsg!s:<7} E ('
            f'{num_error_asserts!s:<3} e, '
            f'{num_open_asserts!s:<3} o, '
            f'{num_unknown_asserts!s:<3} u)'
        )

    return [dict(
        exploit_path=os.path.relpath(exploit_path),
        exploit_type='dynamic',
        num_error_asserts=num_error_asserts,
        num_open_asserts=num_open_asserts,
        num_unknown_asserts=num_unknown_asserts,
        num_open_integrates=num_open_integrates,
        num_closed_integrates=num_closed_integrates,
        result_asserts=amsg,
        result_integrates=imsg,
        is_synced=is_synced,
    )]


def are_exploits_synced__static(subs: str, exp_name: str) -> List[dict]:
    """Check if exploits results are the same as on Integrates."""
    logger.info()
    logger.info('Static exploits:')

    results: List[dict] = []

    bb_fernet_key: str = _get_bb_fernet_key(subs)
    bb_resources = _get_bb_resources(subs, 'static')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/forces/static/exploits/*.exp')):
        exploit_path = os.path.join(os.getcwd(), exploit_path)
        exploit_output_path = f'{exploit_path}.out.yml'

        if (exp_name or '') not in exploit_path:
            logger.debug(f'skipped: {exploit_path}')
            continue

        finding_id = \
            utils.forces.scan_exploit_for_kind_and_id(exploit_path)[1]

        if not utils.integrates.does_finding_exist(finding_id):
            logger.error(f'This finding does not exist at integrates!')
            logger.error(f'  finding_id: {finding_id}')
            logger.error(f'  exploit_path: {exploit_path}')
            continue

        results.extend(_validate_one_static_exploit(
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources,
            exploit_output_path=exploit_output_path,
            exploit_path=exploit_path,
            finding_id=finding_id,
            subs=subs,
        ))

    return results


def are_exploits_synced__dynamic(subs: str, exp_name: str) -> List[dict]:
    """Check if exploits results are the same as on Integrates."""
    logger.info()
    logger.info('Dynamic exploits:')
    results: List[dict] = []

    bb_aws_role_arns: Tuple[str, ...] = _get_bb_aws_role_arns(subs)
    bb_fernet_key: str = _get_bb_fernet_key(subs)
    bb_resources = _get_bb_resources(subs, 'dynamic')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/forces/dynamic/exploits/*.exp')):
        exploit_path = os.path.join(os.getcwd(), exploit_path)
        exploit_output_path = f'{exploit_path}.out.yml'

        if (exp_name or '') not in exploit_path:
            logger.debug(f'skipped: {exploit_path}')
            continue

        finding_id = \
            utils.forces.scan_exploit_for_kind_and_id(exploit_path)[1]

        if not utils.integrates.does_finding_exist(finding_id):
            logger.error(f'This finding does not exist at integrates!')
            logger.error(f'  finding_id: {finding_id}')
            logger.error(f'  exploit_path: {exploit_path}')
            continue

        results.extend(_validate_one_dynamic_exploit(
            bb_aws_role_arns=bb_aws_role_arns,
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources,
            exploit_output_path=exploit_output_path,
            exploit_path=exploit_path,
            finding_id=finding_id,
            subs=subs,
        ))

    return results


def print_nomenclature():
    """Impure function to show the used nomenclature."""
    logger.info('Nomenclature:')
    logger.info()
    logger.info('  E: Exploit')
    logger.info('  I: Integrates')
    logger.info()
    logger.info('  c: closed')
    logger.info('  e: error')
    logger.info('  o: open')
    logger.info('  u: unknown')
    logger.info()
    logger.info('Something is synced if:')
    logger.info('  (E) has no (e), and #(o) on (I) equals #(o) on (E)')


def are_exploits_synced(subs: str, exp_name: str) -> bool:
    """Check if exploits results are the same as on Integrates."""
    utils.generic.aws_login(f'continuous-{subs}')

    config = utils.forces.get_config(subs)
    config = config['schedules']['synchronization']

    # Always run locally, and conditionally on the CI
    should_run_static = \
        not utils.generic.is_env_ci() or config['static']['run']
    should_run_dynamic = \
        not utils.generic.is_env_ci() or config['dynamic']['run']

    # Let users know what are we talking about
    print_nomenclature()

    # Perform some clean up
    patch_file = _get_patch_file_name(subs)
    with open(patch_file, 'w'):
        # Empty the file or create it if it does not exist
        pass

    # If we didn't run, assume it's synced
    results_static: List[dict] = []
    if should_run_static:
        results_static = are_exploits_synced__static(subs, exp_name)
        _print_results_summary(results_static)
    else:
        logger.warn()
        logger.warn('Ignoring Static check due to subscription config')

    # If we didn't run, assume it's synced
    results_dynamic: List[dict] = []
    if should_run_dynamic:
        results_dynamic = are_exploits_synced__dynamic(subs, exp_name)
        _print_results_summary(results_dynamic)
    else:
        logger.warn()
        logger.warn('Ignoring Dynamic check due to subscription config')

    with open(f'check-sync-results.{subs}.json.stream', 'w') as results_handle:
        for json_obj in results_static + results_dynamic:
            json_obj.update(dict(
                datetime=datetime.now().strftime(constants.DATE_FORMAT),
                pipeline_id=os.environ.get('CI_PIPELINE_ID', 'unknown'),
                subscription=subs,
            ))
            results_handle.write(json.dumps({
                'stream': 'results',
                'record': json_obj,
            }, sort_keys=True))
            results_handle.write('\n')

    logger.info()
    logger.info(f'Helpful files were generated:')
    logger.info(f'- {patch_file}')
    return True
