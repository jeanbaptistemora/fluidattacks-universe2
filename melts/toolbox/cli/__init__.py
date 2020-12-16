# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

# Standard library
import functools

# Third parties imports
import click

# Local libraries
from toolbox.utils.version import check_new_version
from toolbox import (
    drills,
    utils,
    constants,
    logger,
)

from .misc import misc_management
from .resources import resources_management


def _valid_integrates_token(ctx, param, value):
    assert constants


class ForceUpgrade(click.Group):
    def parse_args(self, ctx, args):
        if (not utils.generic.is_env_ci() and not utils.generic.is_dev_mode()
                and check_new_version()):
            click.echo('There is a new version')
            click.echo('Updating..')
            if utils.version.upgrade():
                click.echo("Melts updated successfully")
            self.invoke = lambda ctx: None
            logger.info('Try the command again')
        else:
            click.Group.parse_args(self, ctx, args)


@click.group(name='entrypoint', cls=ForceUpgrade)
def entrypoint():
    """Main comand line group."""


entrypoint.add_command(resources_management)
entrypoint.add_command(utils.cli.utils_management)
entrypoint.add_command(drills.cli.drills_management)
entrypoint.add_command(misc_management)


def retry_debugging_on_failure(func):
    """Run a function ensuring the debugger output is shown on failures."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # noqa
            from toolbox.api import integrates
            integrates.clear_cache()
            constants.LOGGER_DEBUG = True
            return func(*args, **kwargs)
    return wrapped


@retry_debugging_on_failure
def main():
    """Usual entrypoint."""
    utils.bugs.configure_bugsnag()
    entrypoint()
    return True
