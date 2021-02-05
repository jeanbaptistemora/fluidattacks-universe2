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
    get_git_remotes, upload_report,
)
from forces.apis.git import (
    extract_repo_name, get_repository_metadata,
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
from forces.utils.model import (
    ForcesConfig,
    KindEnum,
)


async def check_remotes(config: ForcesConfig) -> bool:
    api_remotes = await get_git_remotes(config.group)
    is_in_remotes = False
    for remote in api_remotes:
        if extract_repo_name(remote['url']) == config.repository_name:
            if remote['state'] != 'ACTIVE':
                await log('error', 'The %s repository is innactive',
                          config.repository_name)
                return False
            is_in_remotes = True
            break
    if not is_in_remotes:
        await log('error',
                  'The %s repository has not been registered in integrates',
                  config.repository_name)
    return is_in_remotes


async def entrypoint(
    token: str,
    config: ForcesConfig,
) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()
    exit_code = 0
    set_api_token(token)

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=config.repository_path,
    )
    if config.kind in {KindEnum.STATIC, KindEnum.ALL}:
        if not config.repository_name and metadata[
                'git_repo'] != DEFAULT_COLUMN_VALUE:
            config = config._replace(repository_name=metadata['git_repo'])
        elif not config.repository_name and metadata[
                'git_repo'] == DEFAULT_COLUMN_VALUE:
            await log(
                'error',
                ('Could not detect repository name, use'
                 ' --repo-name option to specify it'),
            )
            await log(
                'warning',
                'The vulnerabilities of all repositories will be scanned')
            if config.kind == KindEnum.ALL:
                exit_code = 1
            # else:  temporarily disable
            #     return 1
        metadata['git_repo'] = config.repository_name or metadata['git_repo']
        await log(
            'info',
            f"Running forces on the repository: {config.repository_name}")

        # check if repo is in roots
        if (not await check_remotes(config)
                and config.repository_name is not None
                and config.kind != KindEnum.ALL):
            return 1

    report = await generate_report(config)

    if report['summary']['total'] > 0:
        yaml_report = await generate_report_log(
            copy.deepcopy(report), verbose_level=config.verbose_level)
        await log('info', '\n%s', yaml_report)
    else:
        await log('info',
                  'The current repository has no reported vulnerabilities')

    if output := config.output:
        temp_file.seek(os.SEEK_SET)
        await in_thread(output.write,
                        temp_file.read().decode('utf-8'))
    if config.strict and report['summary']['open']['total'] > 0:
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
