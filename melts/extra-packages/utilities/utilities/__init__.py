"""Package with useful utilities in the development of Forces Exploits."""

import os
from typing import Any, Callable, Dict, List

from fluidasserts.helper import crypto


def guess_repository() -> List[str]:
    """Return the possible names of the current repository"""
    # Base case, no repo name was possible to detect
    repo_names = []

    # Method 1
    # Get the repo name from the remote url in Linux
    repo_names.append(os.popen((
        'basename $(git remote get-url origin) .git '
        '2>/dev/null')).read()[0:-1])

    # Method 2
    # Get the repo name from the name of the parent folder
    repo_names.append(os.path.basename(os.getcwd()))

    return repo_names


def get_repository() -> str:
    """Return the first not empty possible name of the current repository"""
    repo_names = guess_repository()

    for name in repo_names:
        # Name is not empty
        if name.strip():
            return name

    # Default: not empty name found in guess
    return ''


def is_current_dir_in_repositories(*repositories) -> bool:
    """Return True if the current dir is in the list of repositories."""
    return any(repo in repositories for repo in guess_repository())


def generic_static_exploit(check_func: Callable[..., Any],
                           data: Dict[str, List[str]],
                           *args, **kwargs) -> None:
    """Execute 'check_func(file)' over the data dictionary

    Keyword arguments:
    data -- dictionary of repo names mapping to an array of relative files
    check_func -- function that is called with file relative path
                  as an argument
    """
    repositories = list(filter(data.__contains__, guess_repository()))
    repositories.append('')
    files = data.get(repositories[0], [])

    if files:
        for file in filter(os.path.exists, files):
            check_func(file, *args, **kwargs)


def get_secrets() -> crypto.DecryptedYAML:
    """Return the secrets depending on the current context."""
    # This must be set in order to run, if not, raise KeyError
    os.environ['BB_FERNET_KEY']  # noqa

    if 'CURRENT_EXPLOIT_KIND' in os.environ:
        # We are in the local development environment
        kind: str = os.environ['CURRENT_EXPLOIT_KIND']
        if kind == 'static':
            encrypted_yaml_path: str = \
                f'../../forces/{kind}/resources/secrets.yml'
        elif kind == 'dynamic':
            encrypted_yaml_path = \
                f'forces/{kind}/resources/secrets.yml'
        else:
            raise TypeError(
                f'bad CURRENT_EXPLOIT_KIND({kind}) environment variable')
    else:
        # We are in the container
        encrypted_yaml_path = '/resources/secrets.yml'

    secrets = crypto.DecryptedYAML(
        key_b64=os.environ['BB_FERNET_KEY'],
        encrypted_yaml_path=encrypted_yaml_path)

    return secrets


def get_secrets_with_prefix(prefix: str) -> list:
    """Return a filtered list of secrets that have the indicated prefix"""

    secrets = get_secrets().decrypted_data
    filtered_secrets = {}

    for (key, value) in secrets.items():
        if key.startswith(prefix):
            filtered_secrets[key] = value
    if not filtered_secrets.values():
        raise AttributeError(
            f'No secret found with prefix \'{prefix}\'')
    return list(filtered_secrets.values())


def _file_as_list(file_path: str):
    with open(file_path) as file:
        return tuple(role_arn.strip() for role_arn in file.readlines()
                     if role_arn.strip())


def get_aws_arn_roles():
    """Return the roles ARN that the AWS exploits should assume."""

    if os.environ.get('BB_AWS_ROLE_ARNS'):
        return tuple(role_arn.strip()
                     for role_arn in os.environ['BB_AWS_ROLE_ARNS'].split(',')
                     if role_arn.strip())

    aws_role_arns_path = 'forces/dynamic/resources/BB_AWS_ROLE_ARNS.list'

    roles = ()
    if os.path.isfile(aws_role_arns_path):
        roles = _file_as_list(aws_role_arns_path)
    elif os.path.isfile('/resources/BB_AWS_ROLE_ARNS.list'):
        roles = _file_as_list('/resources/BB_AWS_ROLE_ARNS.list')
    else:
        raise Exception(
            'Unable to find roles from file or from environment info')

    return roles
