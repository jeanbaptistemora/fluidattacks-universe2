#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Yesterday's migration did not take into account the slash since
that for the function quote this is a safe character by default.

In this migration, the slash will be correctly encoded

Execution Time:     2020-07-01 12:14 UTC-5
Finalization Time:  2020-07-01 12:16 UTC-5

"""

import os

import bugsnag
import django

django.setup()

from backend.dal import (project as group_dal)

STAGE: str = os.environ['STAGE']


def log(message: str) -> None:
    print(message)
    if STAGE != 'test':
        bugsnag.notify(Exception(message), severity='info')


def encode_slash(res: str) -> str:
    return res.replace('/', '%2F')


def decode_slash(res: str) -> str:
    return res.replace('%2F', '/')


def main() -> None:
    """
    Update resources
    """
    log('Starting migration 0016')
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
            url_enc = encode_slash(url)
            branch = repo.get('branch', '')
            branch_enc = encode_slash(branch)
            # Update only no encoded repositories
            if url != encode_slash(decode_slash(url)):
                if STAGE == 'test':
                    log(f'---\nrepo before: {repo}')
                repo['urlRepo'] = url_enc
                if STAGE == 'test':
                    log(f'---\nrepo after: {repo}')
            elif branch != encode_slash(decode_slash(branch)):
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

            url_enc = encode_slash(url)
            # Update only no encoded environments
            if url != encode_slash(decode_slash(url)):
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
                log(f'Migration 0016: Group {group_name} succesfully encoded')


if __name__ == '__main__':
    main()
