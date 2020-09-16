# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

# Standard library
import functools

# Third parties imports
import click

# Local libraries
from toolbox import (
    drills,
    utils,
)

from .misc import misc_management
from .analytics import analytics_management
from .integrates import integrates_management
from .sorts import sorts_management
from .resources import resources_management
from .forces import forces_management
from .reports import reports_management


def _valid_integrates_token(ctx, param, value):
    from toolbox import constants
    assert constants


@click.group(name='entrypoint')
def entrypoint():
    """Main comand line group."""


entrypoint.add_command(resources_management)
entrypoint.add_command(analytics_management)
entrypoint.add_command(forces_management)
entrypoint.add_command(integrates_management)
entrypoint.add_command(utils.cli.utils_management)
entrypoint.add_command(sorts_management)
entrypoint.add_command(drills.cli.drills_management)
entrypoint.add_command(misc_management)
entrypoint.add_command(reports_management)


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
            return func(*args, **kwargs)
    return wrapped


@retry_debugging_on_failure
def main():
    """Usual entrypoint."""
    entrypoint()
