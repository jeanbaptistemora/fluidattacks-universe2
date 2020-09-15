"""Fluidattacks Forces package."""
from typing import Any
from importlib.metadata import version
from contextlib import suppress
import copy
import os
import textwrap
import uuid

# Third party libraries
import bugsnag
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientResponseError,
)

# Local imports
from forces.apis.integrates import (
    get_api_token_email,
    get_api_token_group,
    set_api_token,
)
from forces.apis.integrates.api import (
    upload_report,
)
from forces.apis.git import (
    get_repository_metadata,
)
from forces.report import (
    generate_report,
    generate_report_log,
)
from forces.utils.aio import (
    unblock,
)
from forces.utils.logs import (
    log,
    LOG_FILE,
)

# contants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def customize_bugsnag_error_reports(notification: Any) -> None:
    # Customize Login required error
    with suppress(LookupError):
        notification.user = {
            'email': get_api_token_email(),
            'name': get_api_token_group()
        }

    if isinstance(notification.exception, (
            ClientConnectorError,
            ClientResponseError,
    )):
        login_error = any([
            err in str(notification.exception)
            for err in ('Login required', 'Access denied')
        ])
        if login_error:
            notification.severity = 'info'
            notification.unhandled = False


bugsnag.before_notify(customize_bugsnag_error_reports)
bugsnag.configure(
    api_key="3625546064ad4b5b78aa0c0c93919fc5",
    project_root=BASE_DIR,
)
bugsnag.start_session()
bugsnag.send_sessions()


async def show_banner() -> None:
    """Show forces banner."""
    header = textwrap.dedent(rf"""
        #     ______
        #    / ____/___  _____________  _____
        #   / /_  / __ \/ ___/ ___/ _ \/ ___/
        #  / __/ / /_/ / /  / /__/  __(__  )
        # /_/    \____/_/   \___/\___/____/
        #
        #  v. {version('forces')}
        #  ___
        # | >>|> fluid
        # |___|  attacks, we hack your software
        #
        """)
    await log('info', '%s', header)


async def entrypoint(token: str, group: str, **kwargs: Any) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()

    strict = kwargs.get('strict', False)
    exit_code = 1 if strict else 0
    set_api_token(token)
    await show_banner()

    report = await generate_report(project=group,
                                   kind=kwargs.get('kind', 'all'))
    yaml_report = await generate_report_log(
        copy.deepcopy(report), verbose_level=kwargs.pop('verbose_level', 3))
    await log('info', '\n%s', yaml_report)

    if kwargs.get('output', None):
        temp_file.seek(os.SEEK_SET)
        await unblock(kwargs['output'].write, temp_file.read().decode('utf-8'))
    if strict:
        if report['summary']['open']['total'] > 0:
            exit_code = 1
    execution_id = str(uuid.uuid4()).replace('-', '')
    metadata = await unblock(
        get_repository_metadata, repo_path=kwargs.get('repo_path', '.'))
    await upload_report(
        project=group,
        execution_id=execution_id,
        exit_code=str(exit_code),
        report=report,
        log_file=temp_file.name,
        strictness='strict' if strict else 'lax',
        git_metadata=metadata,
    )
    return exit_code
