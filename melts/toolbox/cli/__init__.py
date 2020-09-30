# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

# Third parties imports
import click

# Local libraries
from toolbox import (
    drills,
    utils,
)
from toolbox.utils.function import shield

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


def enable_debug():
    from toolbox import constants
    from toolbox.api import integrates
    integrates.clear_cache()
    constants.LOGGER_DEBUG = True


@shield(retries=2, on_retry=enable_debug)
def main():
    """Usual entrypoint."""
    utils.bugs.configure_bugsnag()
    entrypoint()
