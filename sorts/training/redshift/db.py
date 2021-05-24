# Standard library
from contextlib import contextmanager
import os
from typing import Dict, Iterator

# Third party libraries
import click
from psycopg2 import connect
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)

# Local libraries


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = connect(
        dbname=os.environ["REDSHIFT_DATABASE"],
        host=os.environ["REDSHIFT_HOST"],
        password=os.environ["REDSHIFT_PASSWORD"],
        port=os.environ["REDSHIFT_PORT"],
        user=os.environ["REDSHIFT_USER"],
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        cursor: cursor_cls = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    finally:
        connection.close()


def initialize() -> None:
    with db_cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS sorts")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sorts.training (
                timestamp TIMESTAMPTZ,
                model VARCHAR(256),
                features VARCHAR(256),
                precision FLOAT,
                recall FLOAT,
                f_score FLOAT,
                overfit FLOAT,
                tuned_parameters VARCHAR(256)

                PRIMARY KEY (
                    timestamp
                )
            )
            """
        )


def insert(training_result: Dict[str, str]) -> None:
    with db_cursor() as cursor:
        cursor.execute(
            """
                INSERT INTO sorts.training (
                    timestamp,
                    model,
                    features,
                    precision,
                    recall,
                    f_score,
                    overfit,
                    tuned_parameters
                )
                VALUES (
                    get_date(),
                    %(model)s,
                    %(features)s,
                    %(precision)s,
                    %(recall)s,
                    %(f1_score)s,
                    %(overfit)s,
                    %(tuned_parameters)s
                )
            """,
            training_result,
        )


@click.group(
    help="Redshift integration for Sorts. Handle all training results storage",
)
def cli() -> None:
    pass


@cli.command(
    help="Initializes Redshift schema & sorts table to store training results"
)
def init_db() -> None:
    initialize()


@cli.command(
    help=(
        "Delete and create again Redshift schema & sorts "
        "table to store training results"
    )
)
def reset_db() -> None:
    pass  # incoming function


if __name__ == "__main__":
    cli()
