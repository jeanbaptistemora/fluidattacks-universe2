#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This will migrate all the data in fi_project_names table to integrates 

Execution Time:     2020-05-27 18:30 UTC-5
Finalization Time:  2020-05-27 18:30 UTC-5
"""

import argparse
import os
import sys
from typing import (
    Dict,
)

# Setup Django environment to import functions
PROJECT_PATH: str = '/usr/src/app'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')
sys.path.append(PROJECT_PATH)
os.chdir(PROJECT_PATH)

import bugsnag
from backend.dal.internal_project import (
    get_all_project_names
)
from backend.dal.available_group import (
    TABLE as INTEGRATES_TABLE
)

def migrate_all_names(dry_run: bool) -> None:
    """
    Get all groups from fi_project_names and save to integrates
    """
    all_groups = get_all_project_names()
    if dry_run:
        print('Available groups will be added as follows:')
        for group_name in all_groups:
            print('----')
            print('pk: AVAILABLE_GROUP\n'
                  'sk: {}'.format(group_name.upper()))
    else:
        with INTEGRATES_TABLE.batch_writer() as batch:
            for group_name in all_groups:
                    batch.put_item(
                        Item={
                            'pk': 'AVAILABLE_GROUP',
                            'sk': group_name.upper()})
        log(
            'Migration 0004: Available groups succesfully migrated',
            dry_run
        )


def log(message: str, dry_run: bool) -> None:
    if not dry_run:
        bugsnag.notify(Exception(message), severity='info')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', required=False, action='store_true')

    args: Dict[str, bool] = vars(ap.parse_args())
    dry_run: bool = args['dry_run']

    log(
        'Starting migration 0004 to add all group names'
        'to integrates table',
        dry_run
    )
    migrate_all_names(dry_run)
