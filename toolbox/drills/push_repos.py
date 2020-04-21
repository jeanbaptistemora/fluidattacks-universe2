# Standard libraries
from typing import List, Dict, Any

# Third party libraries
import boto3


def s3_cp(
        origin_bucket: str,
        destination_bucket: str,
        origin_path: str,
        destination_path: str):
    """
    Copy objects from origin to destination

    param: origin_bucket: Bucket to get files from
    param: destination_bucket: Bucket to move files to
    param: origin: Location of objects to copy
    param: destination: Location of objects to put
    """
    s3_client = boto3.client('s3')
    kwargs_copy_file: Dict[str, Any] = {
        'Bucket': destination_bucket,
    }
    kwargs_list_objects: Dict[str, Any] = {
        'Bucket': origin_bucket,
        'Prefix': origin_path,
    }
    paginator = s3_client.get_paginator('list_objects_v2')

    for page in paginator.paginate(**kwargs_list_objects):
        try:
            files: List[Dict[str, Any]] = page['Contents']
        except KeyError:
            break
        for current_file in files:
            file_key: str = current_file['Key']
            file_relative_path: str = file_key.replace(origin_path, '')
            kwargs_copy_file['CopySource'] = f'{origin_bucket}/{file_key}'
            kwargs_copy_file['Key'] = f'{destination_path}{file_relative_path}'
            s3_client.copy_object(**kwargs_copy_file)


def s3_ls(bucket: str, path: str) -> List[str]:
    """
    Return a list of directories contained in path

    param: bucket: Bucket to work with
    param: path: Path to look for directories
    """
    s3_client = boto3.client('s3')
    response_raw: List[Dict] = []
    kwargs: Dict[str, Any] = {
        'Bucket': bucket,
        'Prefix': path,
        'Delimiter': '/',
    }
    paginator = s3_client.get_paginator('list_objects_v2')

    for page in paginator.paginate(**kwargs):
        try:
            response_raw += page['CommonPrefixes']
        except KeyError:
            break
    return list(map(lambda x: x['Prefix'], response_raw))


def s3_get_repos(bucket: str, subs: str, repos_type: str) -> List[str]:
    """
    Return a list of active or inactive repos for a subscription

    param: bucket: Bucket to work with
    param: subs: Subscription to obtain repos from
    param: repos_type: active or inactive repos
    """
    path: str = f'{subs}/{repos_type}/'

    repos: List[str] = s3_ls(bucket, path)
    return list(map(lambda x: x.split('/')[-2], repos))
