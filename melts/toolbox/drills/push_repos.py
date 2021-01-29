# Standard libraries
import os
import json
from typing import (
    List,
    Optional,
)
from pathlib import Path

# Third party libaries
import boto3
import git
from git.exc import GitCommandError

# Local libraries
from toolbox.logger import LOGGER
from toolbox.utils import generic
from toolbox.utils.function import shield


def s3_ls(
    bucket: str,
    path: str,
    endpoint_url: Optional[str] = None,
) -> List[str]:
    client = boto3.client('s3', endpoint_url=endpoint_url)

    if not path.endswith('/'):
        path = f'{path}/'

    response = client.list_objects_v2(
        Bucket=bucket,
        Delimiter='/',
        Prefix=path,
    )
    try:
        return list(map(lambda x: x['Prefix'], response['CommonPrefixes']))
    except KeyError as key_error:
        LOGGER.error('Looks like response does not have Common Prefixes:')
        LOGGER.error(key_error)
    except json.decoder.JSONDecodeError as json_decode_error:
        LOGGER.error('Looks like response was not parseable')
        LOGGER.error(json_decode_error)
    return []


def fill_empty_folders(path: str) -> None:
    empty_folders = []
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty_folders.append(root)
    for folder in empty_folders:
        LOGGER.info('Adding .keep at %s', folder)
        Path(folder, '.keep').touch()


def git_optimize_all(path: str) -> bool:
    git_files = Path(path).glob('**/.git')
    LOGGER.info('Git files: %s', git_files)
    git_folders = set(map(lambda x: x.parent, git_files))
    for folder in git_folders:
        LOGGER.info('Git optimize at %s', folder)
        try:
            git.Repo(str(folder), search_parent_directories=True).git.gc(
                '--aggressive', '--prune=all')
        except GitCommandError as exc:
            LOGGER.error('Git optimization has failed at %s: ', folder)
            LOGGER.info(exc.stdout)
            LOGGER.info(exc.stderr)
            return False
    return True


def s3_sync_fusion_to_s3(
    subs: str,
    bucket: str = 'continuous-repositories',
    endpoint_url: Optional[str] = None,
) -> bool:
    fusion_dir: str = f'groups/{subs}/fusion'
    s3_subs_repos_path: str = f'{subs}/'
    kwargs = dict() if generic.is_env_ci() else dict(
        stdout=None,
        stderr=None,
    )

    aws_sync_command: List[str] = [
        'aws', 's3', 'sync',
        '--delete',
        '--sse', 'AES256',
        '--exclude', "*",
        '--include', "*/.git/*",
        fusion_dir, f's3://{bucket}/{s3_subs_repos_path}',
    ]
    # Allow upload empty folders to keep .git structure
    # and avoid errors
    fill_empty_folders(fusion_dir)

    if not generic.is_env_ci():
        if not git_optimize_all(fusion_dir):
            return False

    if endpoint_url:
        aws_sync_command.append('--endpoint')
        aws_sync_command.append(endpoint_url)
    if generic.is_env_ci():
        aws_sync_command.append('--quiet')
    status, stdout, stderr = generic.run_command(
        cmd=aws_sync_command,
        cwd='.',
        env={},
        **kwargs,  # type:ignore
    )
    if status:
        LOGGER.error('Sync from bucket has failed:')
        LOGGER.info(stdout)
        LOGGER.info(stderr)
        return False
    return True


@shield(retries=1)
def main(
    subs: str,
    bucket: str = 'continuous-repositories',
    aws_login: bool = True,
    aws_profile: str = 'continuous-admin',
    endpoint_url: Optional[str] = None,
) -> bool:
    """
    This function does:

    1. Upload all repos from fusion to s3

    param: subs: group to work with
    param: bucket: Bucket to work with
    param: aws_login: where or not to login to aws
    param: aws_profile: which profile-role to use in case aws_login is true
    param: endpoint_url: aws endpoint to send API requests
    """
    passed: bool = True
    if generic.does_subs_exist(subs) and generic.does_fusion_exist(subs):
        if aws_login:
            generic.aws_login(aws_profile)

        LOGGER.info('Syncing repositories')
        passed = passed \
            and s3_sync_fusion_to_s3(subs, bucket, endpoint_url)
    else:
        LOGGER.error('Either the subs or the fusion folder does not exist')
        passed = False

    return passed
