#! usr/bin/env python3

# Standard library
import logging
import sys

# Third parties libraries
import click
import boto3
from botocore.exceptions import ClientError

# Constants
AWS_REGION: str = 'us-east-1'

# Exit codes:
ERROR_129 = '[Error 129] Please check the flags used to run the service'

# Configure logger
logging.basicConfig(format='# [%(levelname)s] %(message)s')
LOGGER: logging.Logger = logging.getLogger('forces')
LOGGER.setLevel(logging.INFO)


def host_command(cmd: str) -> None:
    """Communicate a command to be executed by the host."""
    print(cmd.replace('\n', ' '))
    sys.exit(0)


def aws_sts_get_username(secret_id: str, secret: str) -> str:
    """Return the account holder username"""
    session: boto3.Session = boto3.Session(
        aws_access_key_id=secret_id,
        aws_secret_access_key=secret,
        region_name=AWS_REGION,
    )

    client = session.client('sts')
    caller_identity = client.get_caller_identity()
    username: str = caller_identity['Arn'].rsplit('/', 1)[1]

    return username


def get_forces_token(group: str, key_id: str, secret_key: str) -> str:
    session: boto3.Session = boto3.Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name=AWS_REGION,
    )
    client = session.client('secretsmanager')
    response = client.get_secret_value(SecretId=f'forces-token-{group}')
    return response.get('SecretString')  # type: ignore


def marketing_and_exit() -> None:
    """Return a greeting offering the service and exit."""
    LOGGER.error('  Seems like your token is invalid...')
    LOGGER.error('\n')
    LOGGER.error('  Do you want:')
    LOGGER.error('    - security testing')
    LOGGER.error('    - with human intelligence ')
    LOGGER.error('    - at DevOps speed?')
    LOGGER.error('\n')
    LOGGER.error(
        '  Contact us and improve your security since the very first day')
    LOGGER.error('    https://fluidattacks.com/web/products/asserts/')
    host_command('exit 1')
    sys.exit(1)


@click.command()
@click.option(
    '--id',
    'secret_id',
    help='Your key id for the Forces Service',
    required=True,
)
@click.option(
    '--secret',
    help='Your secret key value for the Forces Service',
    required=True,
)
@click.option(
    '--static',
    help='Run the container for S.A.S.T.',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--dynamic',
    help='Run the container for D.A.S.T.',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--no-strict',
    help='Do not Break the Build if there are security vulnerabilities :(',
    is_flag=True,
    default=False,
    required=False,
)
def main(
    secret_id: str,
    secret: str,
    static: bool,
    dynamic: bool,
    no_strict: bool,
) -> None:
    if not static and not dynamic:
        LOGGER.error('Please set --static or --dynamic flags (or both :)')
        host_command('exit 1')
        sys.exit(1)

    LOGGER.info('Getting customer identity...')
    try:
        username: str = aws_sts_get_username(secret_id, secret)
        group: str = username.replace('break-build-', '')
    except:  # noqa
        marketing_and_exit()
    else:
        LOGGER.info('   Welcome %s!', group)

    try:
        kind = ''
        if dynamic and static:
            kind = ''
        elif dynamic:
            kind = '--dynamic'
        elif static:
            kind = '--static'

        token = get_forces_token(group, secret_id, secret)
        cmd = (f"""
               true \
               && set -o errexit \
               && set -o pipefail \
               && echo "[INFO] Running forces in $PWD" \
               && docker pull fluidattacks/forces:new \
               && docker run -v "$(pwd):/src" \
                  fluidattacks/forces:new forces --token {token} \
                  {'--lax' if no_strict else '--strict'} {kind} \
                  -vvv""")

        LOGGER.info('A Forces API token was found for this group...')
        host_command(cmd)
    except ClientError:
        marketing_and_exit()


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
