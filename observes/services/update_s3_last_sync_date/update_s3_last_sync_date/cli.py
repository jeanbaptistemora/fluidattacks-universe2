# Standard libraries
import json
from typing import IO

# Third party libraries
import click

# Local libraries
from update_s3_last_sync_date import db_client


SINGLE_JOBS = frozenset([
    'formstack',
    'mixpanel_integrates',
    'timedoctor_backup',
    'timedoctor_etl',
    'timedoctor_refresh_token',
    'zoho_crm_etl',
    'zoho_crm_prepare',
])
COMPOUND_JOBS = frozenset([
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
@click.option('--auth', type=click.File('r'), required=True)
@click.option('--job', type=str, required=True)
def single_job(auth: IO[str], job: str) -> None:
    if job in SINGLE_JOBS:
        update_job(auth, job)
    else:
        raise UnknownJob(f'single job: {job}')


@click.command()
@click.option('--auth', type=click.File('r'), required=True)
@click.option('--job', type=str, required=True)
@click.option('--child', type=str, required=True)
def compound_job(auth: IO[str], job: str, child: str) -> None:
    if job in COMPOUND_JOBS:
        mirror(auth, child)
    else:
        raise UnknownJob(f'compound job: {job}')


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(single_job)
main.add_command(compound_job)
