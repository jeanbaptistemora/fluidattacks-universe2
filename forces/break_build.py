#! usr/bin/env python3

# Standard library
from typing import Any
import sys

# Third libraries
import click
import boto3

# Constants
AWS_REGION: str = 'us-east-1'


def aws_sts_get_username(key_id: str, secret_key: str) -> str:
    """Return the account holder username"""
    session: boto3.Session = boto3.Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name=AWS_REGION,
    )
    client = session.client('sts')
    caller_identity = client.get_caller_identity()
    username: str = caller_identity['Arn'].rsplit('/', 1)[1]
    return username


def get_forces_token(group: str, key_id: str, secret_key: str) -> str:
    session: boto3.Session = boto3.Session(aws_access_key_id=key_id,
                                           aws_secret_access_key=secret_key,
                                           region_name=AWS_REGION)
    client = session.client('secretsmanager')
    response = client.get_secret_value(SecretId=f'forces-api-token-{group}')
    return response.get('SecretString')  # type: ignore


@click.command()
@click.option(
    '--id',
    'o_id',
    required=True,
    help='Your key id for the Forces Service',
)
@click.option(
    '--secret',
    'o_secret',
    required=True,
    help='Your secret key value for the Forces Service',
)
@click.option(
    '--no-strict',
    is_flag=True,
    help='Do not Break the Build if there are security vulnerabilities :(',
    default=False,
    required=False,
)
@click.option(
    '--static',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--cpus',
    type=click.INT,
    default=1,
    required=False,
)
@click.option(
    '--dynamic',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--no-image-rm',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--no-container-rm',
    is_flag=True,
    default=False,
    required=False,
)
@click.option(
    '--color',
    is_flag=True,
    default=False,
    required=False,
)
@click.option('--sub-folder', required=False)
@click.option(
    '--aws-role-arns',
    required=False,
    default='',
)
@click.option(
    '--gitlab-docker-socket-binding',
    is_flag=True,
    default=False,
    required=False,
)
def main(o_id: str, o_secret: str, no_strict: bool, **_: Any) -> None:
    group = aws_sts_get_username(o_id, o_secret).split('-')[-1]
    token = get_forces_token(group, o_id, o_secret)
    print(
        f"forces --token {token} {'--lax' if no_strict else '--strict'} -vvv")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
