import click
from contextlib import (
    contextmanager,
)
import csv
import os
from psycopg2 import (
    connect,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
import tempfile
from training.constants import (
    S3_BUCKET,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
)


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
                    tuned_parameters VARCHAR(256),

                    PRIMARY KEY (
                        timestamp
                    )
                );
                CREATE TABLE IF NOT EXISTS sorts.dataset (
                    timestamp TIMESTAMPTZ,
                    n_rows INTEGER,

                    PRIMARY KEY (
                        timestamp
                    )
                );
                CREATE TABLE IF NOT EXISTS sorts.models (
                    timestamp TIMESTAMPTZ,
                    model VARCHAR(256),
                    features VARCHAR(256),
                    f_score INT,
                    tuned_parameters VARCHAR(256),

                    PRIMARY KEY (
                        timestamp
                    )
                )
            """
        )


def delete(table: str) -> None:
    with db_cursor() as cursor:
        cursor.execute(f"TRUNCATE TABLE sorts.{table}")


def insert(table: str, item: Dict[str, Any]) -> None:
    query_columns: str = ",\n".join(item.keys())
    query_values: str = ",\n".join(f"%({key})s" for key in item.keys())
    with db_cursor() as cursor:
        cursor.execute(
            f"""
                INSERT INTO sorts.{table} (
                    timestamp,
                    {query_columns}
                )
                VALUES (
                    getdate(),
                    {query_values}
                )
            """,
            item,
        )


def reset() -> None:
    """
    First deletes all info in our training table and
    then we iterate each training .csv to refill it.
    Result is that we have our table updated with the last results
    """
    delete("training")
    redshift_table_columns: List[str] = [
        "model",
        "features",
        "precision",
        "recall",
        "f_score",
        "overfit",
        "tuned_parameters",
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        for obj in S3_BUCKET.objects.filter(Prefix="training-output/results"):
            if obj.key.endswith(".csv"):
                filename: str = os.path.basename(obj.key)
                local_file: str = os.path.join(tmpdir, filename)
                S3_BUCKET.download_file(obj.key, local_file)

        for file in os.listdir(tmpdir):
            print(f"[INFO] Updating {file.split('_')[0]} training info...")
            with open(os.path.join(tmpdir, file), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    item = dict(zip(redshift_table_columns, row.values()))
                    item["tuned_parameters"] = ", ".join(
                        item["tuned_parameters"]
                    )
                    insert("training", item)


@click.group(
    help="Redshift integration for Sorts. Handles all Sorts stored data"
)
def cli() -> None:
    pass


@cli.command(help="Initializes Redshift schema & Sorts tables")
def init_db() -> None:
    initialize()


@cli.command(help="Delete and create again Redshift schema & Sorts tables")
def reset_db() -> None:
    reset()


if __name__ == "__main__":
    cli()
