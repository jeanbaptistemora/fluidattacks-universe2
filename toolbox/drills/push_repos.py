# Standard libraries
import os
import json
from typing import List

# Local libraries
from toolbox import logger
from toolbox.utils import generic


def s3_ls(bucket: str, path: str, endpoint_url: str = None) -> List[str]:
    if not path.endswith('/'):
        path = f'{path}/'
    command: List[str] = [
        'aws',
        's3api',
        'list-objects-v2',
        '--bucket',
        bucket,
        '--prefix',
        path,
        '--delimiter',
        '/',
    ]
    if endpoint_url:
        command.append('--endpoint')
        command.append(endpoint_url)

    _, stdout, _ = generic.run_command(
        cmd=command,
        cwd='.',
        env={},
    )
    response = json.loads(stdout)
    return list(map(lambda x: x['Prefix'], response['CommonPrefixes']))


def s3_mv_active_to_inactive(
        subs: str,
        bucket: str = 'continuous-repositories',
        endpoint_url: str = None) -> bool:
    fusion_dir: str = f'subscriptions/{subs}/fusion'
    s3_subs_active_repos_path: str = f'{subs}/active/'
    s3_subs_active_repos: List[str] = \
        s3_ls(bucket, s3_subs_active_repos_path, endpoint_url)
    local_repos: List[str] = os.listdir(fusion_dir)
    kwargs = dict() if generic.is_env_ci() else dict(
        stdout=None,
        stderr=None,
    )

    for s3_active_repo in s3_subs_active_repos:
        s3_active_repo_name: str = s3_active_repo.split('/')[-2]
        if s3_active_repo_name not in local_repos:
            logger.info(f'Move: {s3_active_repo_name} to inactive')
            command: List[str] = [
                'aws',
                's3',
                'mv',
                f's3://{bucket}/{subs}/active/{s3_active_repo_name}',
                f's3://{bucket}/{subs}/inactive/{s3_active_repo_name}',
                '--recursive',
            ]
            if endpoint_url:
                command.append('--endpoint')
                command.append(endpoint_url)
            status, stdout, stderr = generic.run_command(
                cmd=command,
                cwd='.',
                env={},
                **kwargs,
            )
            if status:
                logger.error('Move from bucket has failed:')
                logger.info(stdout)
                logger.info(stderr)
                return False
    return True


def s3_sync_fusion_to_s3(
        subs: str,
        bucket: str = 'continuous-repositories',
        endpoint_url: str = None) -> bool:
    fusion_dir: str = f'subscriptions/{subs}/fusion'
    s3_subs_active_repos_path: str = f'{subs}/active/'
    kwargs = dict() if generic.is_env_ci() else dict(
        stdout=None,
        stderr=None,
    )
    command: List[str] = [
        'aws',
        's3',
        'sync',
        fusion_dir,
        f's3://{bucket}/{s3_subs_active_repos_path}',
        '--sse',
        'AES256',
        '--delete'
    ]
    if endpoint_url:
        command.append('--endpoint')
        command.append(endpoint_url)
    status, stdout, stderr = generic.run_command(
        cmd=command,
        cwd='.',
        env={},
        **kwargs,
    )
    if status:
        logger.error('Sync from bucket has failed:')
        logger.info(stdout)
        logger.info(stderr)
        return False
    return True


def main(
        subs: str,
        bucket: str = 'continuous-repositories',
        aws_login: bool = True,
        aws_profile: str = 'continuous-admin',
        endpoint_url: str = None) -> bool:
    """
    This function does two main things:

    1. Move repos that were not found in fusion from active to inactive
    2. Upload all repos from fusion to s3/active

    param: subs: Subscription to work with
    param: bucket: Bucket to work with
    param: aws_login: where or not to login to aws
    param: aws_profile: which profile-role to use in case aws_login is true
    param: endpoint_url: aws endpoint to send API requests
    """
    passed: bool = True
    if generic.does_subs_exist(subs) and generic.does_fusion_exist(subs):
        if aws_login:
            generic.aws_login(aws_profile)

        logger.info('Checking inactive repositories')
        passed = passed \
            and s3_mv_active_to_inactive(subs, bucket, endpoint_url)

        logger.info('Syncing active repositories')
        passed = passed \
            and s3_sync_fusion_to_s3(subs, bucket, endpoint_url)
    else:
        logger.error(f'Either the subs or the fusion folder does not exist')
        passed = False
    return passed
