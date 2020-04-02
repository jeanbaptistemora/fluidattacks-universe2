# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

# Standard library
import os
import sys

# Third parties imports
import click

# Local libraries
from toolbox import resources


def _valid_integrates_token(ctx, param, value):
    from toolbox import constants
    assert constants


def _valid_subscription(ctx, param, subs):
    if subs not in os.listdir('subscriptions'):
        msg = f'the subscription {subs} does not exist'
        raise click.BadParameter(msg)
    return subs


@click.group()
def cli():
    """Main comand line group."""


@click.command(name='resources')
@click.argument('subscription', default='kloes', callback=_valid_subscription)
@click.option(
    '--mailmap',
    '-mp',
    is_flag=True,
    help='check if the mailmap of a subscription is valid')
@click.option(
    '--clone',
    is_flag=True,
    help='lone the repositories of a subscription',
)
@click.option(
    '--finger-print',
    is_flag=True,
    help='get the fingerprint of a subscription')
@click.option(
    '--edit-secrets', is_flag=True, help='read the secrets of a subscription')
@click.option(
    '--read-secrets', is_flag=True, help='edit the secrets of a subscription')
def resources_manage(mailmap, clone, finger_print, subscription, edit_secrets,
                     read_secrets):
    """Allows administration tasks within subscriptions"""
    if mailmap:
        sys.exit(1 if resources.check_mailmap(subscription) else 1)
    elif clone:
        sys.exit(1 if resources.repo_cloning(subscription) else 1)
    elif finger_print:
        sys.exit(1 if resources.get_fingerprint(subscription) else 1)
    elif edit_secrets:
        sys.exit(0 if resources.edit_secrets(subscription) else 1)
    elif read_secrets:
        sys.exit(0 if resources.read_secrets(subscription) else 1)


@click.command(name='check', short_help='perform checks')
@click.option(
    '--integrates-api-token',
    '-it',
    envvar='INTEGRATES_API_TOKEN',
    help='Check if the token for the integrates api is valid.',
    callback=_valid_integrates_token)
def perform_checks(integrates_api_token, sync):
    """
    Perform a suit of checks.
    """


cli.add_command(resources_manage)
cli.add_command(perform_checks)


def main():
    """Usual entrypoint."""
    cli()
