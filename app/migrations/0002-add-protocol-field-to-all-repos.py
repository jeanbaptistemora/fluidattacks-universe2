#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This migration is needed to add the protocol field to some repositories that
do not have it, probably due to an incomplete migration when the field was
implemented.
Mssing this field causes some actions like activating/deactivating a repository
to end in failure

Execution Time:     2020-05-19 19:35 UTC-5
Finalization Time:  2020-05-13 19:37 UTC-5
"""

import argparse
import hashlib
import json
import os
import sys
from typing import (
    cast,
    Dict,
    List,
    Tuple
)
from urllib.parse import ParseResult, urlparse

# Setup Django environment to import functions
PROJECT_PATH: str = '/usr/src/app'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')
sys.path.append(PROJECT_PATH)
os.chdir(PROJECT_PATH)

import bugsnag
from backend.dal.project import (
    get_all as get_all_projects, TABLE as PROJECT_TABLE
)
from backend.typing import (
    Project as ProjectType,
    Resource as ResourceType
)


def get_default_protocol(project: ProjectType) -> str:
    """
    If the protocol cannot be extracted from the URL, use the most common
    protocol across the project's resources
    """
    protocol_count: Dict[str, int] = {
        'HTTPS': 0,
        'SSH': 0
    }
    for repo in cast(List[ResourceType], project['repositories']):
        protocol: str = cast(str, repo.get('protocol', ''))
        if protocol:
            protocol_count[protocol] += 1
    return max(protocol_count, key=protocol_count.get)


def get_repositories_hash(repositories: List[ResourceType]) -> str:
    return hashlib.sha512(json.dumps(repositories).encode()).hexdigest()


def has_repos_without_protocol(project: ProjectType) -> bool:
    result: bool = False
    for repo in cast(List[ResourceType], project.get('repositories', [])):
        if not repo.get('protocol', ''):
            result = True
            break
    return result


def process_repos(project: ProjectType, default_protocol: str,
        execute: bool) -> Tuple[List[ResourceType], str]:
    allowed_protocols: List[str] = ['SSH', 'HTTPS']
    repos: List[ResourceType] = cast(List[ResourceType], project['repositories'])

    field_hash: str = ''
    if not execute:
        field_hash = get_repositories_hash(repos)

    for repo in repos:
        if not repo.get('protocol', ''):
            repo_url: ParseResult = urlparse(cast(str, repo['urlRepo']))
            protocol: str = default_protocol
            if repo_url.scheme and \
                    repo_url.scheme.upper() in allowed_protocols:
                protocol = repo_url.scheme.upper()
            repo.update({'protocol': protocol})

    return repos, field_hash


def add_protocol_to_repos(project: ProjectType, default_protocol: str,
        execute: bool, dry_run: bool) -> None:
    project_name: str = cast(str, project['project_name'])
    if execute:
        old_field_hash: str = cast(str, project['repositories-hash'])
        current_field_hash: str = get_repositories_hash(
            cast(List[ResourceType], project['repositories']))
        processed_repos: List[ResourceType] = cast(
            List[ResourceType], project['repositories-new'])
        if old_field_hash != current_field_hash:
            processed_repos, _ = process_repos(project, default_protocol, execute)
        response = PROJECT_TABLE.update_item(
                Key={'project_name': project_name},
                UpdateExpression='SET #attr1Name = :val1 REMOVE #attr2Name, #attr3Name',
                ExpressionAttributeNames={
                    '#attr1Name': 'repositories',
                    '#attr2Name': 'repositories-new',
                    '#attr3Name': 'repositories-hash'
                },
                ExpressionAttributeValues={
                    ':val1': processed_repos
                }
            )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            log(
                'Migration 0002: Repositories successfully migrated for '
                'project {}'.format(project_name),
                dry_run
            )
    else:
        repos, field_hash = process_repos(project, default_protocol, execute)
        if dry_run:
            print('Repositories from project {} will be changed '
                  'as follows:'.format(project_name))
            for repo in repos:
                print('----')
                for key, value in repo.items():
                    print('    {}: {}'.format(key, value))
            print('    {}'.format(field_hash))
        else:
            response = PROJECT_TABLE.update_item(
                Key={'project_name': project_name},
                UpdateExpression='SET #attr1Name = :val1, #attr2Name = :val2',
                ExpressionAttributeNames={
                    '#attr1Name': 'repositories-new',
                    '#attr2Name': 'repositories-hash'
                },
                ExpressionAttributeValues={
                    ':val1': repos,
                    ':val2': field_hash
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                log(
                    'Migration 0002: Protocol successfully added to repos of '
                    'project {}'.format(project_name),
                    dry_run
                )


def log(message: str, dry_run: bool) -> None:
    if not dry_run:
        bugsnag.notify(Exception(message), severity='info')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', required=False, action='store_true')
    ap.add_argument('--execute', required=False, action='store_true')

    args: Dict[str, bool] = vars(ap.parse_args())
    dry_run: bool = args['dry_run']
    execute: bool = args['execute']

    log(
        'Starting migration 0002 to ensure all repositories '
        'have protocol field',
        dry_run
    )

    for project in get_all_projects():
        if has_repos_without_protocol(project):
            default_protocol: str = get_default_protocol(project)

            log(
                'Migration 0002: processing project {} with default protocol '
                '{}'.format(project['project_name'], default_protocol),
                dry_run
            )

            add_protocol_to_repos(project, default_protocol, execute, dry_run)
