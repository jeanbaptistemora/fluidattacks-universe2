# Standard libraries
import os
from typing import List

# Third party libraries
import ruamel.yaml as yaml

# Local libraries
from toolbox.drills import generic as drills_generic
from toolbox.utils.function import shield, RetryAndFinallyReturn
from toolbox import (
    logger,
    utils,
)


def notify_out_of_scope(include_regexps, exclude_regexps) -> bool:
    logger.info('Please remember the scope:')
    logger.info('  In scope:')
    for regex in include_regexps:
        logger.info(f'    - {regex}')

    if exclude_regexps:
        logger.info()
        logger.info('  Out of scope:')
        for regex in exclude_regexps:
            logger.info(f'    - {regex}')

    logger.info()

    return True


def delete_out_of_scope_files(group: str) -> bool:
    path_to_fusion: str = os.path.join('groups', group, 'fusion')
    path_to_config: str = os.path.join('groups', group, 'config', 'config.yml')

    with open(path_to_config) as config_handle:
        config_obj: dict = yaml.safe_load(config_handle)

    include_regexps = tuple(
        rule['regex'] for rule in config_obj['coverage']['lines']['include'])
    exclude_regexps = tuple(
        rule['regex'] for rule in config_obj['coverage']['lines']['exclude'])

    non_matching_files_iterator = utils.file.iter_non_matching_files(
        path=path_to_fusion,
        include_regexps=include_regexps,
        exclude_regexps=exclude_regexps,
    )

    for path in non_matching_files_iterator:
        path = os.path.join(path_to_fusion, path)
        if '.git' not in path:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                os.removedirs(path)

    return notify_out_of_scope(include_regexps, exclude_regexps)


def pull_repos_s3_to_fusion(subs: str,
                            local_path: str,
                            repository_name: str = 'all') -> bool:
    '''
    Download repos from s3 to a provided path

    param: subs: group to work with
    param: local_path: Path to store downloads
    '''

    if repository_name != 'all':
        local_path = f'{local_path}/{repository_name}'
    else:
        repository_name = ''

    bucket_path: str = f's3://continuous-repositories/' \
        f'{subs}/{repository_name}'

    os.makedirs(local_path, exist_ok=True)

    aws_sync_command: List[str] = [
        'aws', 's3', 'sync',
        '--delete',
        '--sse', 'AES256',
        bucket_path, local_path,
    ]

    git_expand_repositories_command: List[str] = [
        'find', local_path,
        '-name', '.git',
        '-execdir',
        'git', 'checkout',
        '--', '.', ';'
    ]
    logger.info(f'Downloading {subs} repositories')

    # Passing None to stdout and stderr shows the s3 progress
    # We want the CI to be as quiet as possible to have clean logs
    kwargs = dict() if utils.generic.is_env_ci() else dict(
        stdout=None,
        stderr=None,
    )

    status, stdout, stderr = utils.generic.run_command(
        cmd=aws_sync_command,
        cwd='.',
        env={},
        **kwargs,
    )

    if status:
        logger.error('Sync from bucket has failed:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False

    git_status, git_stdout, git_stderr = utils.generic.run_command(
        cmd=git_expand_repositories_command,
        cwd='.',
        env={},
        **kwargs,
    )

    if git_status:
        logger.error('Expand repositories has failed:')
        logger.info(git_stdout)
        logger.info(git_stderr)
        logger.info()
        return False
    return True


@shield(retries=1)
def main(subs: str, repository_name: str = 'all') -> bool:
    '''
    Clone all repos for a group

    param: subs: group to work with
    '''
    bucket: str = 'continuous-repositories'
    passed: bool = True
    if not utils.generic.does_subs_exist(subs):
        logger.error(f'group {subs} does not exist.')
        passed = False
        return passed

    utils.generic.aws_login(f'continuous-{subs}')

    if not drills_generic.s3_path_exists(bucket, f'{subs}/'):
        logger.error(f'group {subs} does not have repos uploaded to s3')
        passed = False
    else:
        local_path: str = f'groups/{subs}/fusion/'

        logger.info('Computing last upload date')
        days: int = \
            drills_generic.calculate_days_ago(
                drills_generic.get_last_upload(bucket, f'{subs}/'))

        passed = passed \
            and pull_repos_s3_to_fusion(subs, local_path, repository_name) \
            and delete_out_of_scope_files(subs)

        logger.info(f'Data for {subs} was uploaded to S3 {days} days ago')

    if not passed:
        raise RetryAndFinallyReturn(passed)

    return passed
