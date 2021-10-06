#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
This will migrate all the data in fi_project_names table to integrates

Execution Time:     2020-05-27 18:30 UTC-5
Finalization Time:  2020-05-27 18:30 UTC-5
"""
import argparse
import bugsnag
from names.dal import (
    get_all as get_all_group_names,
    TABLE_NAME as INTEGRATES_TABLE,
)
from typing import (
    Dict,
)


def migrate_all_names(dry_run: bool) -> None:
    """
    Get all groups from fi_project_names and save to integrates
    """
    all_groups = get_all_group_names("group")
    if dry_run:
        print("Available groups will be added as follows:")
        for group_name in all_groups:
            print("----")
            print(f"pk: AVAILABLE_GROUP\nsk: {group_name.upper()}")
    else:
        with INTEGRATES_TABLE.batch_writer() as batch:
            for group_name in all_groups:
                batch.put_item(
                    Item={"pk": "AVAILABLE_GROUP", "sk": group_name.upper()}
                )
        log("Migration 0004: Available groups succesfully migrated", dry_run)


def log(message: str, dry_run: bool) -> None:
    if not dry_run:
        bugsnag.notify(Exception(message), severity="info")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", required=False, action="store_true")

    args: Dict[str, bool] = vars(ap.parse_args())
    dry_run_flag: bool = args["dry_run"]

    log(
        "Starting migration 0004 to add all group names to integrates table",
        dry_run_flag,
    )
    migrate_all_names(dry_run_flag)
