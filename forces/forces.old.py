#! usr/bin/env python3

# Standard library
import re
import sys
import argparse
import textwrap
import traceback
import contextlib

# Third parties libraries
import boto3
from botocore.exceptions import ClientError

# Constants
AWS_REGION: str = 'us-east-1'

# Exit codes:
ERROR_129 = '[Error 129] Please check the flags used to run the service'


def notify(*args, **kwargs):
    """Print to stderr."""
    kwargs.update({'file': sys.stderr})
    print(*args, **kwargs)
    return True


def host_comment(cmd: str):
    """Comunicate a command to the host, but it's never executed."""
    print(textwrap.indent(textwrap.dedent(cmd), '# ', lambda x: True))


def host_command(cmd: str):
    """Communicate a command to be executed by the host."""
    print(cmd.replace('\n', ' '))
    sys.exit(0)


def parse_args_from_cli():
    """Parse the arguments from the CLI."""
    parser = argparse.ArgumentParser(
        prog='Forces',
        epilog=textwrap.dedent("""
            Use in your pipeline environment:

                $ docker pull fluidattacks/forces
                $ bash <(docker run fluidattacks/forces --help)
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--id',
        help='Your key id for the Forces Service',
        required=True)
    parser.add_argument(
        '--secret',
        help='Your secret key value for the Forces Service',
        required=True)
    parser.add_argument(
        '--static',
        help='Run the container for S.A.S.T.',
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--dynamic',
        help='Run the container for D.A.S.T.',
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--no-strict',
        help='Do not Break the Build if there are security vulnerabilities :(',
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--cpus',
        help=('Allow the container to use this number of host CPUs, '
              'default 1, use 0 to use all available CPUs'),
        type=int,
        default=1,
        required=False)
    parser.add_argument(
        '--no-image-rm',
        help=('Use this flag to indicate that you do not want to '
              'delete images after execution'),
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--no-container-rm',
        help=('Use this flag to indicate that you do not want to '
              'delete containers after execution, (for security reasons, '
              'containers should always be removed)'),
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--color',
        help='Colorize the execution output',
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--gitlab-docker-socket-binding',
        help=('Use this flag to indicate that you are running on a '
              'GitLab Docker Executor with /var/run/docker.sock binding'),
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        '--sub-folder',
        help='Only execute testing over the given sub-folder',
        required=False)
    parser.add_argument(
        '--aws-role-arns',
        help=('Use this flag to specify the roles ARN that the AWS exploits'
              ' should assume, you can specify one or more comma separated.\n'
              'Expected format: '
              'arn:aws:iam::account-id:role/role-name-with-path'),
        required=False,
        default='')

    return parser.parse_args()


def validate_args(args):
    """Return True if arguments are valid, False otherwise."""
    success: bool = True

    notify(f'Checking Forces parameters...')

    if not args.static and not args.dynamic:
        notify('  Please set --static or --dynamic flags (or both :)')
        success = False

    if args.cpus < 0:
        notify('  Please set --cpus to an integer greater than or equal to 0')
        success = False

    if args.aws_role_arns:
        regex_p = r'arn:(aws[a-zA-Z-]*)?:iam::\d{12}:role\/[a-zA-Z0-9-_\/]*'
        for role in args.aws_role_arns.split(','):
            if not re.match(regex_p, role):
                notify(
                    f'The role {role} does not match with the expected format')
                success = False

    if not success:
        sys.exit(78)

    return args


def marketing_and_exit():
    """Return a greeting offering the service and exit."""
    notify('  Error:')
    notify(textwrap.indent(traceback.format_exc(), '    '))
    notify()
    notify('  Seems like your token is invalid...')
    notify()
    notify('  Do you want:')
    notify('    - security testing')
    notify('    - with human intelligence ')
    notify('    - at DevOps speed?')
    notify()
    notify('  Contact us and improve your security since the very first day')
    notify('    https://fluidattacks.com/web/products/asserts/')
    host_command('exit 1')
    sys.exit(1)


def aws_sts_get_username(args):
    """Return the account holder username"""
    session: boto3.Session = boto3.Session(aws_access_key_id=args.id,
                                           aws_secret_access_key=args.secret,
                                           region_name=AWS_REGION)

    client = session.client('sts')
    caller_identity = client.get_caller_identity()
    username: str = caller_identity['Arn'].rsplit('/', 1)[1]
    return username


def get_forces_token(group: str, key_id: str, secret_key: str) -> str:
    session: boto3.Session = boto3.Session(aws_access_key_id=key_id,
                                           aws_secret_access_key=secret_key,
                                           region_name=AWS_REGION)
    client = session.client('secretsmanager')
    response = client.get_secret_value(SecretId=f'forces-token-{group}')
    return response.get('SecretString')  # type: ignore


def main():  # noqa: MC0001
    """Usual entrypoint."""
    # pylint: disable=too-many-statements
    try:
        with contextlib.redirect_stdout(sys.stderr):
            args = parse_args_from_cli()
            args = validate_args(args)
    except SystemExit:
        notify()
        notify(ERROR_129)
        host_command('exit 129')

    notify()
    notify(f'Getting customer identity...')

    try:
        username: str = aws_sts_get_username(args)
        group: str = username.replace('break-build-', '')
    except:  # noqa
        marketing_and_exit()
    else:
        notify(f'  Welcome {group}!')

    #
    # Bad command usage warning
    #

    host_comment(f"""
        [Warning] If you see this message the command is wrong!

        You are probably using:
            $ docker run fluidattacks/forces ...

        Please add bash in one of the two following ways:
            $ bash <(docker run fluidattacks/forces ...)
            $ docker run fluidattacks/forces ... | bash

        This is because the main docker run command just creates an script
        specific to your operative system, CLI arguments, and environment.
        But it's bash who executes that code.

        Should you have any doubts, please contact us

        Have a nice day!
        """)

    #
    # Validate if a forces api token was deployed for the group
    #
    with contextlib.suppress(ClientError):
        notify()
        kind = 'dynamic' if args.dynamic else (
            'static' if args.static else '')
        token = get_forces_token(group, args.id, args.secret)
        cmd = (f"""
               true \
               && set -o errexit \
               && set -o pipefail \
               && echo "[INFO] Running forces in $PWD" \
               && docker pull fluidattacks/forces:new \
               && current_repo=$(basename "$PWD") \
               && docker run -v "$(pwd):/$current_repo" \
                  --env CI_PROJECT_NAME="${{CI_PROJECT_NAME}}" \
                  --env Build.Repository.Name="${{Build.Repository.Name}}" \
                  -w "/$current_repo" \
                  fluidattacks/forces:new forces --token {token} \
                  --repo-path "/$current_repo" \
                  {'--lax' if args.no_strict else '--strict'} \
                  --{kind} \
                  -vvv""")
        notify('A Forces API token was found for this group...')

    #
    # Send everything to the host
    #

    host_command(cmd)


if __name__ == '__main__':
    main()


# Footnote 1.
#   In GitLab:
#     The host (gitlab-runner),
#       the job's container (user defined),
#       and the job's child containers (forces and ECR)
#     Do not share the root file system.
#     What this implies is that mounting the current working directory
#       (which resides in the job's file system),
#       cannot be done. (It will mount, but empty)
#     To solve this we will load the volumes from the job's container
#       into the child containers, and then copy from the mounted
#       volumes the repository contents to /code
#     See:
#       https://gitlab.com/gitlab-org/gitlab-foss/
#         issues/41227#note_52029664
#       https://medium.com/@patrick.winters/
#          mounting-volumes-in-sibling-containers-with-
#          gitlab-ci-534e5edc4035
#       https://docs.gitlab.com/ee/ci/docker/
#          using_docker_build.html#use-docker-in-docker-
#          workflow-with-docker-executor
#     This approach is compatible with socket binding
#       (mounting /var/run/docker.sock from host to job's container
#        so job's docker commands run in the host's daemon)
#       See:
#         https://docs.gitlab.com/ee/ci/docker/
#           using_docker_build.html#use-docker-socket-binding
