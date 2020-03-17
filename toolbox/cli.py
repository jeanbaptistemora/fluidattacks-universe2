
# Standard library
import os
import re
import sys
import argparse
import functools
from typing import Pattern, Match

# Local libraries
from toolbox import analytics, logger, toolbox, resources

# We need to load some modules at run-time in order to avoid cyclic imports
# pylint: disable=import-outside-toplevel


def retry_debugging_on_failure(func):
    """Run a function ensuring the debugger output is shown on failures."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # noqa
            from toolbox import constants
            from toolbox.api import integrates
            integrates.clear_cache()

            constants.LOGGER_DEBUG = True
            func(*args, **kwargs)
    return wrapped


@retry_debugging_on_failure  # noqa: MC0001
def main():  # noqa
    """Usual entrypoint."""
    starting_dir: str = os.getcwd()

    subs_re: Pattern = re.compile(r'^.*?continuous/subscriptions/(\w+)')
    subs_match: Match = subs_re.match(starting_dir)

    subs: str = str()
    if subs_match:
        subs, = subs_match.groups()
        logger.debug(f'Automatically detected subscription: {subs}')

    if 'TOOLBOX_SKIP_ROOT_DETECTION' not in os.environ:
        if 'continuous' not in starting_dir:
            logger.error(
                'Please run the toolbox inside the continuous repo')
            sys.exit(78)
        while not os.getcwd().endswith('continuous'):
            os.chdir('..')
            logger.debug('Adjusted working dir to:', os.getcwd())

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--analytics-break-build-logs',
        action='store_true',
        required=False,
        help='pipelines-only')
    parser.add_argument(
        '--check-integrates-token',
        action='store_true',
        required=False)
    parser.add_argument(
        '--check-mailmap',
        action='store_true')
    parser.add_argument(
        '--check-sync',
        action='store_true')
    parser.add_argument(
        '--check-uploads',
        action='store_true')
    parser.add_argument(
        '--decrypt-secrets',
        action='store_true')
    parser.add_argument(
        '--does-subs-exist',
        action='store_true')
    parser.add_argument(
        '--edit-secrets',
        action='store_true')
    parser.add_argument(
        '--encrypt-secrets',
        action='store_true')
    parser.add_argument(
        '--exp',
        metavar='name',
        required=False)
    parser.add_argument(
        '--fill-with-mocks',
        action='store_true',
        help='pipelines only')
    parser.add_argument(
        '--generate-exploits',
        action='store_true',
        help='pipelines only')
    parser.add_argument(
        '--get-commit-subs',
        action='store_true',
        help='pipelines only')
    parser.add_argument(
        '--get-exps-fragments',
        action='store_true')
    parser.add_argument(
        '--get-fingerprint',
        action='store_true')
    parser.add_argument(
        '--get-static-dict',
        action='store_true',
        help='privileges required')
    parser.add_argument(
        '--get-vulns',
        action='store_true')
    parser.add_argument(
        '--has-break-build',
        action='store_true')
    parser.add_argument(
        '--init-secrets',
        action='store_true')
    parser.add_argument(
        '--is-valid-commit',
        action='store_true',
        help='pipelines only')
    parser.add_argument(
        '--lint-exps',
        action='store_true')
    parser.add_argument(
        '--okta-aws-login',
        action='store_true')
    parser.add_argument(
        '--read-secrets',
        action='store_true')
    parser.add_argument(
        '--repo-cloning',
        action='store_true')
    parser.add_argument(
        '--report-vulns',
        action='store_true')
    parser.add_argument(
        '--run-dynamic-exps',
        action='store_true')
    parser.add_argument(
        '--run-static-exps',
        action='store_true')
    parser.add_argument(
        '--report-dynamic-exps',
        action='store_true')
    parser.add_argument(
        '--report-static-exps',
        action='store_true')
    parser.add_argument(
        '--check-repos',
        action='store_true')
    parser.add_argument(
        '--email',
        required=False)
    parser.add_argument(
        '--subs',
        metavar='subs',
        default=subs,
        required=False)
    parser.add_argument(
        '--vpn',
        action='store_true')
    parser.add_argument(
        '--sync-repositories-to-aws',
        action='store_true')
    args = parser.parse_args()

    if args.fill_with_mocks:
        toolbox.fill_with_mocks(
            subs_glob=(args.subs or '*'), create_files=True)
    elif args.analytics_break_build_logs:
        sys.exit(0 if analytics.logs.load_executions_to_database() else 1)
    elif args.generate_exploits:
        toolbox.generate_exploits(
            subs_glob=(args.subs or '*'))
    elif args.is_valid_commit:
        sys.exit(0 if toolbox.is_valid_commit() else 1)
    elif args.get_commit_subs:
        subs = toolbox.get_subscription_from_commit_msg()
        print(subs)
        sys.exit(0 if subs else 1)
    elif args.check_integrates_token:
        from toolbox import constants
        assert constants
        sys.exit(0)
    elif args.check_mailmap and not args.subs:
        sys.exit(0 if resources.check_mailmap(os.getcwd()) else 1)
    elif args.get_fingerprint and not args.subs:
        sys.exit(0 if resources.get_fingerprint(os.getcwd()) else 1)
    else:
        # This flags need to know the subscription name
        if args.subs:
            if args.has_break_build:
                sys.exit(0 if toolbox.has_break_build(args.subs) else 1)
            if args.does_subs_exist:
                sys.exit(0 if toolbox.does_subs_exist(args.subs) else 1)
            elif args.run_static_exps:
                sys.exit(0 if toolbox.run_static_exploits(
                    args.subs, args.exp) else 1)
            elif args.run_dynamic_exps:
                sys.exit(0 if toolbox.run_dynamic_exploits(
                    args.subs, args.exp) else 1)
            elif args.report_static_exps:
                sys.exit(0 if toolbox.report_exploits(
                    args.subs, 'static', args.exp) else 1)
            elif args.report_dynamic_exps:
                sys.exit(0 if toolbox.report_exploits(
                    args.subs, 'dynamic', args.exp) else 1)
            elif args.get_exps_fragments:
                sys.exit(0 if toolbox.get_exps_fragments(
                    args.subs, args.exp) else 1)
            elif args.get_vulns:
                sys.exit(0 if toolbox.get_vulnerabilities_yaml(
                    args.subs) else 1)
            elif args.report_vulns:
                sys.exit(0 if toolbox.report_vulnerabilities(
                    args.subs, args.exp) else 1)
            elif args.get_static_dict:
                sys.exit(0 if toolbox.get_static_dictionary(
                    args.subs) else 1)
            elif args.lint_exps:
                sys.exit(0 if toolbox.lint_exploits(
                    args.subs, args.exp) else 1)
            elif args.check_sync:
                sys.exit(0 if toolbox.are_exploits_synced(
                    args.subs, args.exp) else 1)
            elif args.sync_repositories_to_aws:
                sys.exit(0 if resources.sync_repositories_to_aws(
                    args.subs) else 1)
            elif args.check_uploads:
                sys.exit(0 if toolbox.were_exploits_uploaded(args.subs) else 1)
            elif args.init_secrets:
                sys.exit(0 if toolbox.init_secrets(args.subs) else 1)
            elif args.encrypt_secrets:
                sys.exit(0 if toolbox.encrypt_secrets(args.subs) else 1)
            elif args.decrypt_secrets:
                sys.exit(0 if toolbox.decrypt_secrets(args.subs) else 1)
            elif args.repo_cloning:
                sys.exit(0 if resources.repo_cloning(args.subs) else 1)
            elif args.check_mailmap:
                sys.exit(0 if resources.check_mailmap(args.subs) else 1)
            elif args.get_fingerprint:
                sys.exit(0 if resources.get_fingerprint(args.subs) else 1)
            elif args.edit_secrets:
                sys.exit(0 if resources.edit_secrets(args.subs) else 1)
            elif args.read_secrets:
                sys.exit(0 if resources.read_secrets(args.subs) else 1)
            elif args.okta_aws_login:
                sys.exit(0 if resources.utils.okta_aws_login(
                    f'continuous-{args.subs}') else 1)
            elif args.check_repos:
                sys.exit(0 if resources.check_repositories(
                    args.subs) else 1)
            elif args.vpn:
                sys.exit(0 if resources.vpn(args.subs) else 1)
        parser.print_help()
        print()
        print('Note: some methods need the "--subs" flag, or being')
        print('      run from continuous/subscriptions/${proyect}')
        print('Note: many methods accept an optional "--exp name" flag')
        print('      to filter the execution')
        sys.exit(1)
    sys.exit(0)
