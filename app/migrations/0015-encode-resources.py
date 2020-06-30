#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This migration encodes all environments and repositories using urllib
in all groups

Execution Time:     2020-06-30 18:39 UTC-5
Finalization Time:  2020-06-30 18:40 UTC-5

"""

import os
import uuid
from urllib.parse import quote, unquote
import rollbar
import django

django.setup()

from backend.dal import (project as group_dal)

STAGE: str = os.environ['STAGE']


def log(message: str) -> None:
    print(message)
    if STAGE != 'test':
        rollbar.report_message(message, level='debug')


def main() -> None:
    """
    Assign organization to every user
    """
    log('Starting migration 0015')
    all_groups = group_dal.get_all(
        filtering_exp= 'attribute_exists(environments) or \
            attribute_exists(repositories)',
        data_attr='project_name,environments,repositories')

    if STAGE == 'test':
        log('Resources will be updated as follows:')

    for group in all_groups:
        group_name = group.get('project_name')

        if STAGE == 'test':
            log(f'---\nGroup: {group_name}')

        repos = group.get('repositories', [])
        for repo in repos:
            url = repo.get('urlRepo', '')
            url_enc = quote(url)
            branch = repo.get('branch', '')
            branch_enc = quote(branch)
            # Update only no encoded repositories
            if url != quote(unquote(url)):
                if STAGE == 'test':
                    log(f'---\nrepo before: {repo}')
                repo['urlRepo'] = url_enc
                if STAGE == 'test':
                    log(f'---\nrepo after: {repo}')
            elif branch != quote(unquote(branch)):
                if STAGE == 'test':
                    log(f'---\nrepo before: {repo}')
                repo['branch'] = branch_enc
                if STAGE == 'test':
                    log(f'---\nrepo after: {repo}')

            else:
                if STAGE == 'test':
                    log(f'---\nrepo is already encoded: {repo}')

        envs = group.get('environments', [])
        for env in envs:
            url = env.get('urlEnv', '')

            url_enc = quote(url)
            # Update only no encoded environments
            if url != quote(unquote(url)):
                if STAGE == 'test':
                    log(f'---\nenv before: {env}')

                env['urlEnv'] = url_enc

                if STAGE == 'test':
                    log(f'---\nenv after: {env}')
            else:
                if STAGE == 'test':
                    log(f'---\nenv is already encoded: {env}')
                
        if STAGE != 'test':
            success : bool = group_dal.update(
                project_name=group_name,
                data={'environments': envs, 'repositories': repos}    
            )
            if success:
                log(f'Migration 0015: Group {group_name} succesfully encoded')


if __name__ == '__main__':
    main()
