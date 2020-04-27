# Standard libraries
import os
from typing import List, Dict, Any

# Third party libraries
import boto3

# Local libraries
from toolbox import logger
from toolbox.utils import generic


def s3_rm(bucket: str, path: str, endpoint_url: str = None):
    """
    Remove objects in path

    param: bucket: Bucket to work with
    param: path: Path to remove
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    kwargs_list_objects: Dict[str, Any] = {
        'Bucket': bucket,
        'Prefix': path,
    }
    files_raw: List[Dict[str, Any]]
    files_parsed: List[Dict[str, str]]
    kwargs_delete_objects: Dict[str, Any]
    paginator = s3_client.get_paginator('list_objects_v2')

    logger.info(f'Remove: {bucket}::{path}')
    for page in paginator.paginate(**kwargs_list_objects):
        try:
            files_raw = page['Contents']
        except KeyError:
            break
        files_parsed = list(map(lambda x: {'Key': x['Key']}, files_raw))
        kwargs_delete_objects = {
            'Bucket': bucket,
            'Delete': {'Objects': files_parsed, 'Quiet': True},
        }
        s3_client.delete_objects(**kwargs_delete_objects)


def s3_cp(
        origin_bucket: str,
        dest_bucket: str,
        origin_path: str,
        dest_path: str,
        endpoint_url: str = None):
    """
    Copy objects from origin to destination

    param: origin_bucket: Bucket to get files from
    param: dest_bucket: Bucket to move files to
    param: origin: Location of objects to copy
    param: dest: Location of objects to put
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    kwargs_copy_file: Dict[str, Any] = {
        'Bucket': dest_bucket,
    }
    kwargs_list_objects: Dict[str, Any] = {
        'Bucket': origin_bucket,
        'Prefix': origin_path,
    }
    paginator = s3_client.get_paginator('list_objects_v2')

    logger.info(
        f'Copy: {origin_bucket}::{origin_path} to {dest_bucket}::{dest_path}'
    )
    for page in paginator.paginate(**kwargs_list_objects):
        try:
            files: List[Dict[str, Any]] = page['Contents']
        except KeyError:
            break
        for current_file in files:
            file_key: str = current_file['Key']
            file_relative_path: str = file_key.replace(origin_path, '')
            kwargs_copy_file['CopySource'] = f'{origin_bucket}/{file_key}'
            kwargs_copy_file['Key'] = f'{dest_path}{file_relative_path}'
            s3_client.copy_object(**kwargs_copy_file)


def s3_ls(bucket: str, path: str, endpoint_url: str = None) -> List[str]:
    """
    Return a list of directories contained in path

    param: bucket: Bucket to work with
    param: path: Path to look for directories
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
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


def s3_upload(
        bucket: str,
        origin_path: str,
        dest_path: str,
        endpoint_url: str = None):
    """
    Upload files from local to s3 bucket

    param: bucket: Bucket to work with
    param: origin_path: path of files to upload
    param: dest_path: s3 path to upload files
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)

    logger.info(f'Upload: {origin_path} to {bucket}::{dest_path}')
    for root, _, files in os.walk(origin_path):
        for filename in files:
            file_origin_path: str = f'{root}/{filename}'.replace('//', '/')
            file_dest_path: str = \
                file_origin_path.replace(root, dest_path)
            s3_client.upload_file(
                file_origin_path,
                bucket,
                file_dest_path
            )


def s3_get_repos(
        bucket: str,
        subs: str,
        repos_type: str,
        endpoint_url: str = None) -> List[str]:
    """
    Return a list of active or inactive repos for a subscription

    param: bucket: Bucket to work with
    param: subs: Subscription to obtain repos from
    param: repos_type: active or inactive repos
    param: endpoint_url: aws endpoint to send API requests
    """
    path: str = f'{subs}/{repos_type}/'

    repos: List[str] = s3_ls(bucket, path, endpoint_url)
    return list(map(lambda x: x.split('/')[-2], repos))


def main(
        subs: str,
        bucket: str = 'continuous-repositories',
        aws_login: bool = True,
        profile: str = 'continuous-admin',
        endpoint_url: str = None) -> bool:
    """
    This function does three main things:

    1. Upload all repos from fusion to s3/active
    2. Remove all inactive repos that became active again
    3. Move repos that were not found in fusion from active to inactive

    param: subs: Subscription to work with
    param: bucket: Bucket to work with
    param: aws_login: where or not to login to aws
    param: profile: which profile-role to use in case aws_login is true
    param: endpoint_url: aws endpoint to send API requests
    """
    if generic.does_subs_exist(subs) and generic.does_fusion_exist(subs):
        fusion_dir: str = f'subscriptions/{subs}/fusion'
        remote_repos_active: List[str] = \
            s3_get_repos(bucket, subs, 'active', endpoint_url)
        remote_repos_inactive: List[str] = \
            s3_get_repos(bucket, subs, 'inactive', endpoint_url)
        local_repos: List[str] = os.listdir(fusion_dir)
        origin_path: str
        dest_path: str

        if aws_login:
            generic.aws_login(profile)
        logger.info('Checking active repositories')
        for repo in local_repos:
            origin_path = f'{fusion_dir}/{repo}/'
            dest_path = f'{subs}/active/{repo}/'
            s3_upload(bucket, origin_path, dest_path, endpoint_url)
            if repo in remote_repos_inactive:
                logger.info(f'{repo} from inactive is now active')
                s3_rm(bucket, f'{subs}/inactive/{repo}/', endpoint_url)

        logger.info('Checking inactive repositories')
        for repo in remote_repos_active:
            if repo not in local_repos:
                logger.info(f'Moving {repo} to inactive')
                origin_path = f'{subs}/active/{repo}/'
                dest_path = f'{subs}/inactive/{repo}/'
                s3_cp(bucket, bucket, origin_path, dest_path, endpoint_url)
                s3_rm(bucket, origin_path, endpoint_url)
        return True
    logger.error(f'Either the subs or the fusion folder does not exist')
    return False
