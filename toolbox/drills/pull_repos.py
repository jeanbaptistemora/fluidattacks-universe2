# Standard libraries
import os
from typing import List
from datetime import datetime

# Local libraries
from toolbox.drills import generic as drills_generic
from toolbox.utils import generic as utils_generic
from toolbox import logger


def pull_repos_s3_to_fusion(subs: str, local_path: str) -> bool:
    '''
    Download repos from s3 to a provided path

    param: subs: Subscription to work with
    param: local_path: Path to store downloads
    '''
    bucket_path: str = f's3://continuous-repositories/{subs}/active/'
    os.makedirs(local_path, exist_ok=True)
    sync_command: List[str] = ['aws', 's3', 'sync', bucket_path, local_path,
                               '--sse', 'AES256']
    logger.info(f'Dowloading {subs} repositories')
    status, stdout, stderr = utils_generic.run_command(
        cmd=sync_command,
        cwd='.',
        env={})
    if status:
        logger.error('Sync from bucket has failed:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False
    return True


def main(subs: str) -> bool:
    '''
    Clone all repos for a subscription

    param: subs: Subscription to work with
    '''
    bucket: str = 'continuous-repositories'
    passed: bool = True
    if not utils_generic.does_subs_exist(subs):
        logger.error(f'Subscription {subs} does not exist.')
        passed = False
        return passed

    utils_generic.aws_login(f'continuous-{subs}')

    if not drills_generic.s3_path_exists(bucket, f'{subs}/'):
        logger.error(f'Subscription {subs} does not have repos uploaded to s3')
        passed = False
    else:
        local_path: str = f'subscriptions/{subs}/fusion/'
        last_upload_date: datetime = \
            drills_generic.get_last_upload(bucket, f'{subs}/')
        days: int = drills_generic.calculate_days_ago(last_upload_date)
        passed = passed and pull_repos_s3_to_fusion(subs, local_path)
        logger.info(f'Subscription {subs} was last updated {days} days ago')
    return passed
