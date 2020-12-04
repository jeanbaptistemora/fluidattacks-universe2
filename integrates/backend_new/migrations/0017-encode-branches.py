#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Yesterday's migration did not take into account the slash since
that for the function quote this is a safe character by default.

In this migration, the slash will be correctly encoded

Execution Time:     2020-07-01 13:14 UTC-5
Finalization Time:  2020-07-01 13:16 UTC-5

"""

import os
from urllib.parse import quote, unquote

import bugsnag
import django

django.setup()

from backend.dal import (project as group_dal)

STAGE: str = os.environ['STAGE']


def log(message: str) -> None:
    print(message)
    if STAGE != 'test':
        bugsnag.notify(Exception(message), severity='info')


def main() -> None:
    """
    Update resources
    """
    log('Starting migration 0017')
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
            branch = repo.get('branch', '')
            branch_enc = quote(branch, safe='')
            # Update previously not encoded branches
            if (url == quote(unquote(url), safe='') and
                branch != quote(unquote(branch), safe='')):
                if STAGE == 'test':
                    log(f'---\nrepo before: {repo}')
                repo['branch'] = branch_enc
                if STAGE == 'test':
                    log(f'---\nrepo after: {repo}')

        if STAGE != 'test':
            success : bool = group_dal.update(
                project_name=group_name,
                data={'repositories': repos}    
            )
            if success:
                log(f'Migration 0017: Group {group_name} succesfully encoded')


if __name__ == '__main__':
    main()
