"""Fluidattacks Forces package."""
# Standar imports
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
    DEFAULT_COLUMN_VALUE,
)
from forces.report import (
    generate_report,
    generate_report_log,
)
from forces.utils.logs import (
    log,
    LOG_FILE,
)
from forces.utils.model import ForcesConfig


async def entrypoint(
    token: str,
    config: ForcesConfig,
) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=config.repository_path,
    )
    if not config.repository_name and metadata[
            'git_repo'] != DEFAULT_COLUMN_VALUE:
        config = config._replace(repository_name=metadata['git_repo'])

    await log('info',
              f"Running forces on the repository: {config.repository_name}")
    exit_code = 0
    set_api_token(token)

    report = await generate_report(config)

    yaml_report = await generate_report_log(
        copy.deepcopy(report), verbose_level=config.verbose_level)
    await log('info', '\n%s', yaml_report)

    if output := config.output:
        temp_file.seek(os.SEEK_SET)
        await in_thread(output.write,
                        temp_file.read().decode('utf-8'))
    if config.strict:
        if report['summary']['open']['total'] > 0:
            exit_code = 1
    execution_id = str(uuid.uuid4()).replace('-', '')
    await log('info', 'Success execution: %s', exit_code == 0)
    success_upload = await upload_report(
        project=config.group,
        execution_id=execution_id,
        exit_code=str(exit_code),
        report=report,
        log_file=temp_file.name,
        strictness='strict' if config.strict else 'lax',
        git_metadata=metadata,
        kind=config.kind.value,
    )
    await log('info', 'Success upload metadata execution: %s', success_upload)
    return exit_code
