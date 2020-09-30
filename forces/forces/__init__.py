"""Fluidattacks Forces package."""
from typing import Any
import copy
import os
import uuid

# Third party libraries
from aioextensions import in_thread
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
from forces.utils.logs import (
    log,
    LOG_FILE,
)


async def entrypoint(token: str, group: str, **kwargs: Any) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=kwargs.get('repo_path', '.'),
    )

    await log('info',
              f"Running forces on the repository: {metadata['git_repo']}")
    strict = kwargs.get('strict', False)
    exit_code = 0
    set_api_token(token)

    report = await generate_report(
        project=group,
        kind=kwargs.get('kind', 'all'),
        repo_name=kwargs.pop('repo_name', None),
    )

    yaml_report = await generate_report_log(
        copy.deepcopy(report), verbose_level=kwargs.pop('verbose_level', 3))
    await log('info', '\n%s', yaml_report)

    if kwargs.get('output', None):
        temp_file.seek(os.SEEK_SET)
        await in_thread(kwargs['output'].write,
                        temp_file.read().decode('utf-8'))
    if strict:
        if report['summary']['open']['total'] > 0:
            exit_code = 1
    execution_id = str(uuid.uuid4()).replace('-', '')
    await log('info', 'Success execution: %s', exit_code == 0)
    success_upload = await upload_report(
        project=group,
        execution_id=execution_id,
        exit_code=str(exit_code),
        report=report,
        log_file=temp_file.name,
        strictness='strict' if strict else 'lax',
        git_metadata=metadata,
        kind=kwargs.get('kind', 'all'),
    )
    await log('info', 'Success upload metadata execution: %s', success_upload)
    return exit_code
