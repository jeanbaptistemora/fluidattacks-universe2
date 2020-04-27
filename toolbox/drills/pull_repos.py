# Standard libraries
import os
from typing import List, Dict, Any
from datetime import datetime
from pytz import UTC

# Third party libraries
import boto3

# Local libraries
from toolbox.utils import generic
from toolbox import logger


def calculate_days_ago(date: datetime) -> int:
    '''
    Return passed days after a provided date

    param: date: provided date to calculate passed days
    '''
    passed_days = \
        datetime.utcnow() - date.replace(tzinfo=UTC)
    return passed_days.days


def s3_path_exists(bucket: str, path: str, endpoint_url: str = None) -> bool:
    '''
    Return True if provided path exists within a bucket. Else otherwise

    param: bucket: Bucket to work with
    param: path: Path to verify existance within bucket
    param: endpoint_url: aws endpoint to send API requests
    '''
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    kwargs_list_objects: Dict[str, Any] = {
        'Bucket': bucket,
        'Prefix': path,
    }
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(**kwargs_list_objects):
        return page.get('Contents') is not None
    return False


def get_last_upload(
        bucket: str,
        path: str,
        endpoint_url: str = None) -> datetime:
    '''
    Get upload date of last uploaded file in a path

    param: bucket: Bucket to work with
    param: path: Path to look for newest file
    param: endpoint_url: aws endpoint to send API requests
    '''
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    kwargs_list_objects: Dict[str, Any] = {
        'Bucket': bucket,
        'Prefix': path,
    }
    last_modified: datetime = datetime(2000, 1, 1).replace(tzinfo=UTC)
    files_raw: List[Dict[str, Any]]

    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(**kwargs_list_objects):
        try:
            files_raw = page['Contents']
        except KeyError:
            break
        for filename in files_raw:
            if last_modified < filename['LastModified']:
                last_modified = filename['LastModified']
    return last_modified


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
    '''
    Clone all repos for a subscription

    param: subs: Subscription to work with
    '''
    bucket: str = 'continuous-repositories'
    passed: bool = True
    if not generic.does_subs_exist(subs):
        logger.error(f'Subscription {subs} does not exist.')
        passed = False
    elif not s3_path_exists(bucket, f'{subs}/'):
        logger.error(f'Subscription {subs} does not have repos uploaded to s3')
        passed = False
    else:
        local_path: str = f'subscriptions/{subs}/fusion/'
        last_upload_date: datetime = get_last_upload(bucket, f'{subs}/')
        days: int = calculate_days_ago(last_upload_date)
        generic.aws_login(f'continuous-{subs}')
        passed = passed and pull_repos_s3_to_fusion(subs, local_path)
        logger.info(f'Subscription {subs} was last updated {days} days ago')
    return passed
