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
    constants,
)

from .misc import misc_management
from .resources import resources_management


@click.group(name='entrypoint')
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
