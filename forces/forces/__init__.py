"""Fluidattacks Forces package."""
from typing import Any
import copy
import uuid

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


async def entrypoint(token: str, group: str, **kwargs: Any) -> int:
    """Entrypoint function"""
    exit_code = 0
    set_api_token(token)

    report = await generate_report(project=group)
    yaml_report = await generate_report_log(
        copy.deepcopy(report), verbose_level=kwargs.pop('verbose_level', 3))

    if kwargs.get('output', None):
        await unblock(kwargs['output'].write, yaml_report)
    else:
        print(yaml_report)
    if kwargs.get('strict', False):
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
