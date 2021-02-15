# Standard libraries
import json
from typing import IO, Optional

# Third party libraries
import click

# Local libraries
from update_s3_last_sync_date import db_client


no_group_jobs = frozenset([
    'formstack',
    'mixpanel_integrates',
    'zoho_crm_etl',
    'zoho_crm_prepare',
])
group_jobs = frozenset([
    'mirror',
])


class UnknownJob(Exception):
    pass


class MissingOption(Exception):
    pass


def update_job(auth_file: IO[str], job_name: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update_job(db_state, job_name)
    finally:
        db_client.drop_access_point(db_state)


def mirror(auth_file: IO[str], group: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update_group(db_state, group, 'last_sync_date')
    finally:
        db_client.drop_access_point(db_state)


@click.command()
@click.argument('job-name', type=str)
@click.option('--auth-file', type=click.File('r'), required=True)
@click.option('--group', type=str, default=None)
def main(
    auth_file: IO[str],
    job_name: str,
    group: Optional[str]
) -> None:
    if job_name in no_group_jobs:
        update_job(auth_file, job_name)
    elif job_name in group_jobs:
        if not group:
            raise MissingOption(f'--group is required for job `{job_name}`')
        mirror(auth_file, group)
    else:
        raise UnknownJob(job_name)
