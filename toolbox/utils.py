# Standard library
import os
import io
import re
import sys
import glob
import datetime
import configparser
import textwrap
import functools
import subprocess
import contextlib
from pathlib import Path
from typing import Tuple

# Third parties libraries
import dateutil.parser
import requests
from pykwalify.core import Core
from pykwalify.errors import SchemaError
from ruamel.yaml import YAML, safe_load

# Local libraries
from toolbox import logger, helper, constants


def is_env_ci() -> bool:
    """
    Check if environment is local or CI.
    Return True if CI.
    Return False if local.
    """
    return bool(os.environ.get('CI'))


def is_branch_master() -> bool:
    """
    Check if branch is master or dev.
    Return True if branch is master.
    Return False if branch is dev.
    """
    return os.environ.get('CI_COMMIT_REF_NAME') == 'master'


def run_command(cmd: str, cwd: str, env: dict) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout and stderr."""
    # We are checking the exit code via proc.returncode
    #   in the upstream component
    # pylint: disable=subprocess-run-check
    proc = subprocess.run(cmd,
                          cwd=cwd,
                          env={**os.environ.copy(), **env},
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True)
    return proc.returncode, proc.stdout, proc.stderr


def okta_aws_configure_role(role: str, profile: str = 'default'):
    """
    Set okta-awscli profile in ~/.okta-aws config file
    for logging in as a specific role.
    """
    url = 'fluidattacks.okta.com'
    applink = f'https://{url}/home/amazon_aws/0oa1ju1nmaERwnuYW357/272'
    config_role = f'arn:aws:iam::205810638802:role/{role}'
    okta_aws_config = configparser.ConfigParser()
    Path(f"{os.environ['HOME']}/.okta-aws").touch()
    with open(f"{os.environ['HOME']}/.okta-aws", 'r') as store_file:
        okta_aws_config.read_file(store_file)
        if not okta_aws_config.has_section(profile):
            okta_aws_config.add_section(profile)
        okta_aws_config[profile]['base-url'] = url
        okta_aws_config[profile]['app-link'] = applink
        okta_aws_config[profile]['role'] = config_role
    with open(f"{os.environ['HOME']}/.okta-aws", 'w') as store_file:
        okta_aws_config.write(store_file)


def okta_aws_login(profile: str = 'default') -> bool:
    """
    Login to AWS through OKTA using a specific profile
    """
    logger.info('Logging in to Okta.')
    okta_aws_configure_role(profile, profile)
    success = subprocess.call(
        f'okta-awscli --profile {profile} --okta-profile {profile}',
        shell=True
    )
    os.environ['AWS_ACCESS_KEY_ID'] = \
        os.popen(f'aws configure get {profile}.aws_access_key_id') \
        .read().rstrip()
    os.environ['AWS_SECRET_ACCESS_KEY'] = \
        os.popen(f'aws configure get {profile}.aws_secret_access_key') \
        .read().rstrip()
    os.environ['AWS_SESSION_TOKEN'] = \
        os.popen(f'aws configure get {profile}.aws_session_token') \
        .read().rstrip()
    return success == 0


def aws_login(profile: str = 'default'):
    """
    Login as either:
    1. AWS Prod if branch is master in CI
    2. AWS Dev if branch is dev in CI
    3. Okta AWS if local integration
    """
    if is_env_ci():
        if is_branch_master():
            os.environ['AWS_ACCESS_KEY_ID'] = \
                os.environ['PROD_AWS_ACCESS_KEY_ID']
            os.environ['AWS_SECRET_ACCESS_KEY'] = \
                os.environ['PROD_AWS_SECRET_ACCESS_KEY']
        else:
            os.environ['AWS_ACCESS_KEY_ID'] = \
                os.environ['DEV_AWS_ACCESS_KEY_ID']
            os.environ['AWS_SECRET_ACCESS_KEY'] = \
                os.environ['DEV_AWS_SECRET_ACCESS_KEY']
        cmd_access_key = \
            'aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID'
        cmd_secret_key = \
            'aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY'
        run_command(cmd=cmd_access_key, cwd='.', env={})
        run_command(cmd=cmd_secret_key, cwd='.', env={})
    else:
        okta_aws_login(profile)


@functools.lru_cache(maxsize=None, typed=True)
def get_sops_secret(var: str, path: str, profile: str = 'default') -> str:
    """
    Get a key from a sops file.
    """
    if is_env_ci():
        profile = 'default'
    cmd = f'sops --aws-profile {profile} -d --extract \'["{var}"]\' {path}'
    code, stdout, stderr = run_command(cmd=cmd, cwd='.', env={})
    if code:
        logger.error('while calling sops:')
        logger.error('  stdout:')
        logger.error(textwrap.indent(stdout, '    '))
        logger.error('  stderr:')
        logger.error(textwrap.indent(stderr, '    '))
        sys.exit(78)
    return stdout


def _load_vulns_schema():
    url = ('https://gitlab.com/fluidattacks/integrates/-/raw/6a6d743f3dfbd3c'
           'b5b41f7bdce7c194d89f7acd3/django-apps/integrates-back/backend/'
           'entity/schema.yaml')
    response = requests.get(url)
    yaml = YAML()
    return yaml.load(response.text)


def validate_vulns_file_schema(file_url: str) -> bool:
    """Validate if a vulnerabilities file has the correct schema."""
    core = Core(source_file=file_url, schema_data=_load_vulns_schema())
    is_valid = False
    try:
        core.validate(raise_exception=True)
        with open(file_url, 'r') as reader:
            first_line = reader.readline()
            if any(map(lambda x: x in first_line, ['{}', '-'])):
                is_valid = False
                logger.error(file_url)
                logger.error('Empty schema.')
            else:
                is_valid = True
    except SchemaError:
        logger.error('An error occurred validating vulnerabilities file.')

    return is_valid


def iter_vulns_path(subs: str, vulns_name: str, run_kind: str = 'all'):
    """
    Create a interable for vulns path and exploit path of a subscription.

    yields (vulns_path, exploit_path).
    """
    for vulns_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/*/exploits/*.exp.vulns.yml')):

        kind = vulns_path.split('/')[3]
        if not run_kind == kind and run_kind != 'all':
            continue

        exploit_path = vulns_path.replace('.vulns.yml', '')

        if not (vulns_name or '') in vulns_path:
            logger.info(f'skipped: {vulns_path}')
            continue

        if os.stat(vulns_path).st_size == 0:
            logger.info(vulns_path)
            logger.info('  ', 'Empty')
            continue
        if not validate_vulns_file_schema(vulns_path):
            continue

        yield (vulns_path, exploit_path)


def iter_exploit_paths(subscription: str):
    """
    Create a generator for the exploits of a subscription.

    :parameter subscription: Subscription name.

    yields exploit_path.
    """
    for exploit_path in glob.glob(
            f'subscriptions/{subscription}/break-build/*/*/*.exp'):
        yield exploit_path


def iter_subscritions_config():
    """
    Create a generator for config of subscriptions.

    yields subscription_configuration.
    """
    for config_path in glob.glob('subscriptions/*/config/config.yml'):
        yield safe_load(open(config_path))


@contextlib.contextmanager
def output_block(*, indent=2):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), \
            contextlib.redirect_stderr(buffer):
        yield
    print(textwrap.indent(buffer.getvalue(), ' ' * indent))


def guess_date_from_str(
    date_str: str,
    default: str = '2000-01-01T00:00:00Z',
) -> str:
    """Use heuristics to transform any-format string into an RFC 3339 date."""
    try:
        date_obj = dateutil.parser.parse(date_str)
    except (ValueError, OverflowError):
        return default
    else:
        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


def rfc3339_str_to_date_obj(
    date_str: str,
) -> datetime.datetime:
    """Parse an RFT3339 formatted string into a datetime object."""
    return dateutil.parser.parse(date_str)


def get_commit_message():
    """Return commit message."""
    return os.popen('git log --max-count 1 --format=%s').read()[:-1]


def get_files_in_commit():
    """Return modified files in actual commit."""
    return os.popen(
        'git show --name-only --pretty="" $(git rev-parse HEAD)').read().split(
            '\n')[:-1]


def valid_commit_exp():
    commit_msg = get_commit_message()

    pattern = r'(\w+)\((exp)\):\s#([0-9.]*)\s(\w+)\s?([a-z-]*)'

    if '(exp)' not in commit_msg:
        return True

    matchs: list = re.search(pattern, commit_msg)
    groups = matchs.groups() if matchs else None

    if not groups or (len(groups) == 4 and groups[0] == 'fix'
                      and groups[4] not in constants.EXP_LABELS):
        return False

    proj = groups[3]
    changed_files = get_files_in_commit()

    exploits = [
        path for path in changed_files
        if path.split('/')[4] == 'exploits' and path.split('/')[1] == proj
    ]

    return len(exploits) == 1


def get_modified_exps():
    """Returns the finding id of the exploits modified in the commit."""
    findigs = []
    for path in get_files_in_commit():
        if '/exploits/' in path:
            _, find = helper.forces.scan_exploit_for_kind_and_id(path)
            findigs.append(find)
    return findigs
