import click
from job_last_success import (
    db_client,
)
from job_last_success.conf import (
    COMPOUND_JOBS,
    COMPOUND_JOBS_TABLES,
    SINGLE_JOBS,
)
import json
from typing import (
    IO,
)


class UnknownJob(Exception):
    pass


class MissingOption(Exception):
    pass


def update_single_job(auth_file: IO[str], job_name: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.single_job_update(db_state, job_name)
    finally:
        db_client.drop_access_point(db_state)


def update_compound_job(auth_file: IO[str], job: str, child: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.compound_job_update(
            db_state, child, COMPOUND_JOBS_TABLES[job]
        )
    finally:
        db_client.drop_access_point(db_state)


@click.command()
@click.option("--auth", type=click.File("r"), required=True)
@click.option("--job", type=str, required=True)
def single_job(auth: IO[str], job: str) -> None:
    if job in SINGLE_JOBS or job.startswith("skims"):
        update_single_job(auth, job)
    else:
        raise UnknownJob(f"single job: {job}")


@click.command()
@click.option("--auth", type=click.File("r"), required=True)
@click.option("--job", type=str, required=True)
@click.option("--child", type=str, required=True)
def compound_job(auth: IO[str], job: str, child: str) -> None:
    if job in COMPOUND_JOBS:
        update_compound_job(auth, job, child)
    else:
        raise UnknownJob(f"compound job: {job}")


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(single_job)
main.add_command(compound_job)
