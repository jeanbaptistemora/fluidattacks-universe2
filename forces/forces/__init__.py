"""Fluidattacks Forces package."""
from typing import Any
import copy
import os
import uuid

# Third party libraries
import bugsnag
from gql.transport.exceptions import (
    TransportQueryError,
)

# Local imports
from forces.apis.integrates import (
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

# contants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def customize_bugsnag_error_reports(notification: Any) -> None:
    # Customize Login required error
    if isinstance(notification.exception, TransportQueryError):
        login_error = any([
            err.get('message') in ('Login required', 'Access denied')
            for err in notification.exception.errors
        ])
        if login_error:
            notification.severity = 'info'
            notification.unhandled = False


bugsnag.before_notify(customize_bugsnag_error_reports)
bugsnag.configure(
    api_key="3625546064ad4b5b78aa0c0c93919fc5",
    project_root=BASE_DIR,
)


async def entrypoint(token: str, group: str, **kwargs: Any) -> int:
    """Entrypoint function"""
    strict = kwargs.get('strict', False)
    exit_code = 1 if strict else 0
    set_api_token(token)

    report = await generate_report(project=group)
    yaml_report = await generate_report_log(
        copy.deepcopy(report), verbose_level=kwargs.pop('verbose_level', 3))

    if kwargs.get('output', None):
        await unblock(kwargs['output'].write, yaml_report)
    else:
        print(yaml_report)
    if strict:
        if report['summary']['open'] > 0:
            exit_code = 1
    execution_id = str(uuid.uuid4()).replace('-', '')
    metadata = await unblock(
        get_repository_metadata, repo_path=kwargs.get('repo_path', '.'))
    await upload_report(
        project=group,
        execution_id=execution_id,
        exit_code=str(exit_code),
        report=report,
        log=yaml_report,
        strictness='strict' if kwargs.get('strict', False) else 'lax',
        git_metadata=metadata,
    )
    return exit_code
