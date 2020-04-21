# Standard libraries
import os
from typing import List

# Local libraries
from toolbox.utils import generic
from toolbox import logger


def pull_repos_s3_to_fusion(subs: str, local_path: str) -> bool:
    bucket_path: str = f's3://continuous-repositories/{subs}/active/'
    os.makedirs(local_path, exist_ok=True)
    sync_command: List[str] = ['aws', 's3', 'sync', bucket_path, local_path,
                               '--sse', 'AES256']
    logger.info(f'Dowloading {subs} repositories')
    status, stdout, stderr = generic.run_command(
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
    if generic.does_subs_exist(subs):
        local_path: str = f'subscriptions/{subs}/fusion/'
        generic.aws_login(f'continuous-{subs}')
        return pull_repos_s3_to_fusion(subs, local_path)
    logger.error(f'Subscription {subs} does not exist.')
    return False
