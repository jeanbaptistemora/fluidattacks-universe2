# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

from botocore.exceptions import (
    ClientError,
)
import click
import functools
from git.exc import (
    GitCommandError,
    GitError,
    InvalidGitRepositoryError,
)
import json
import sys
from toolbox import (
    constants,
    drills,
    utils,
)
from toolbox.api.exceptions import (
    IntegratesError,
)
from toolbox.cli.misc import (
    misc_management,
)
from toolbox.cli.resources import (
    resources_management,
)
from toolbox.logger import (
    LOGGER,
)
from typing import (
    Any,
    Callable,
)


@click.group(name="melts")
def melts() -> None:
    """Main comand line group."""


melts.add_command(resources_management)
melts.add_command(utils.cli.utils_management)
melts.add_command(drills.cli.drills_management)
melts.add_command(misc_management)


def retry_debugging_on_failure(func: Callable[..., Any]) -> Callable[..., Any]:
    """Run a function ensuring the debugger output is shown on failures."""

    @functools.wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Callable[..., Any]:
        try:
            return func(*args, **kwargs)
        except (
            ClientError,
            GitCommandError,
            GitError,
            FileNotFoundError,
            IndexError,
            IntegratesError,
            InvalidGitRepositoryError,
            json.decoder.JSONDecodeError,
            KeyError,
            OverflowError,
            ValueError,
        ) as exc:  # noqa
            from toolbox.api import (
                integrates,
            )

            LOGGER.error(exc)
            integrates.clear_cache()
            constants.LOGGER_DEBUG = True
            return func(*args, **kwargs)

    return wrapped


@retry_debugging_on_failure
def main() -> bool:
    """Usual entrypoint."""
    utils.bugs.configure_bugsnag()
    melts(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
        prog_name="$ m f /melts",
    )
    return True


if __name__ == "__main__":
    main()
