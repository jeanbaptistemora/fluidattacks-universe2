from datetime import (
    datetime,
)
import logging
import psycopg2 as postgres
from target_redshift.utils import (
    PGCURR,
    str_len,
    stringify,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

LOG = logging.getLogger(__name__)


class Batcher:
    """A class that wraps a Redshift query executor.

    Args:
        dbcon: The database connection.
        dbcur: The database cursor.
        schema_name: The schema to operate over.

    Attributes:
        initt: Class's instantiation timestamp.
        dbcon: The database connection.
        dbcur: The database cursor.
        sname: Schema name over which the Class is operating.
        buckets: An object that stores the queued statements.

    Public methods:
        ex: Executes a statement on the database.
        queue: Queue a row to be loaded into a table.
        load: Loads a batch of queued rows into a table.
        flush: Loads batches queued for all tables.
        vacuum: Vacuums loaded tables to improve query performance.

    Raises:
        postgres.ProgrammingError: When a query was corrupted.
        Status information from time to time.
    """

    def __init__(self, dbcur: PGCURR, schema_name: str) -> None:
        LOG.info("INFO: worker up at %s.", datetime.utcnow())

        self.initt: float = time.time()

        self.dbcur: PGCURR = dbcur

        self.msize: int = 0
        self.rsize: int = 0

        self.sname: str = schema_name
        self.fields: Dict[str, List[str]] = {}
        self.buckets: Dict[str, Any] = {}

    def ex(self, statement: str, do_print: bool = False) -> None:
        """Executes a single statement.

        Args:
            statement: Statement to be run.
            do_print: True if you want to print the statement to stdout.

        Raises:
            postgres.ProgrammingError: When a query was corrupted.
        """
        if do_print:
            LOG.info("EXEC: %s.", statement)
        try:
            self.dbcur.execute(statement)
        except postgres.ProgrammingError as exc:
            LOG.error("EXCEPTION: %s %s", type(exc), exc)

    def set_field_names(self, table_name: str, field_names: List[str]) -> None:
        """Set the fields for the provided table."""
        # Load queued rows in case we are changing the fields to be loaded
        self.load(table_name)

        # Now it's safe to alter the loaded fields
        self.fields[table_name] = field_names

    def queue(self, table_name: str, record: Dict[str, str]) -> None:
        """Queue rows in buckets before pushing them to redshift.

        All values must come here as a string representation.
            see translate_record().
        Values are stored in a bucket as a list of rows.
            a row is a string of its values separated by comma.
        Buckets are automatically loaded when they reach the optimal size.

        Args:
            table_name: Table that owns the rows.
            values: The row's values to be load.
        """

        # initialize the bucket
        if table_name not in self.buckets:
            self.buckets[table_name] = {
                "n_fields": len(self.fields[table_name]),
                "records": [],
                "count": 0,
                "size": 0,
            }

        # turn a row into a string of values separated by comma
        row = stringify(
            [record.get(field, "null") for field in self.fields[table_name]],
            do_group=False,
        )
        row_size = str_len(row)

        # a redshift statement must be less than 16MB
        # also load if there are too many queued data (rows * fields)
        # if we are to exceed the limit with the current row

        n_fields = self.buckets[table_name]["n_fields"]
        n_values = self.buckets[table_name]["count"] + 1
        n_items = n_fields * n_values

        if (
            self.buckets[table_name]["size"] + row_size >= 13000000
            or n_items >= 1000000
        ):
            # load the queued rows to Redshift
            self.load(table_name)

        if self.msize >= 256 * 1024 * 1024 or self.rsize > 1000000:
            self.flush()

        # queues the provided row in this function call
        self.msize += row_size
        self.rsize += 1
        self.buckets[table_name]["records"].append(record)
        self.buckets[table_name]["count"] += 1
        self.buckets[table_name]["size"] += row_size

    def load(self, table_name: str, do_print: bool = False) -> None:
        """Loads a batch of queued rows to redshift.

        Args:
            table_name: Table that owns the rows.
            do_print: True if you want to print the statement to stdout.
        """
        if (
            table_name not in self.fields
            or table_name not in self.buckets
            or self.buckets[table_name]["count"] == 0
        ):
            return

        fields = stringify(
            [f'"{f}"' for f in self.fields[table_name]], do_group=False
        )

        values = stringify(
            [
                stringify(
                    [
                        record.get(field, "null")
                        for field in self.fields[table_name]
                    ],
                    do_group=False,
                )
                for record in self.buckets[table_name]["records"]
            ],
            do_group=True,
        )

        statement = f"""
            INSERT INTO \"{self.sname}\".\"{table_name}\"({fields})
            VALUES {values}"""
        LOG.debug(
            "statement: fields= %s, records=%s, size=%s",
            len(self.fields[table_name]),
            len(self.buckets[table_name]["records"]),
            len(statement.encode("utf-8")),
        )
        self.ex(statement, do_print)

        count = self.buckets[table_name]["count"]
        size = round(self.buckets[table_name]["size"] / 1.0e6, 2)
        LOG.info(
            ("INFO: %s rows (%s MB) loaded to Redshift/%s/%s."),
            count,
            size,
            self.sname,
            table_name,
        )

        self.msize -= self.buckets[table_name]["size"]
        self.rsize -= self.buckets[table_name]["count"]
        self.buckets[table_name]["records"] = []
        self.buckets[table_name]["count"] = 0
        self.buckets[table_name]["size"] = 0

    def flush(self, do_print: bool = False) -> None:
        """Loads to redshift the buckets that din't reach the optimal size.

        Args:
            do_print: True if you want to print the statements to stdout.
        """
        for table_name in self.buckets:
            self.load(table_name, do_print)
        self.msize = 0
        self.rsize = 0

    def vacuum(self, do_print: bool = True) -> None:
        """Vacuums touched tables to improve query performance.

        Args:
            do_print: True if you want to print the statements to stdout.
        """
        vacuum_errors = (
            postgres.ProgrammingError,
            postgres.NotSupportedError,
        )
        for table_name in self.buckets:
            try:
                table_path: str = f'"{self.sname}"."{table_name}"'
                self.ex(
                    f"VACUUM FULL {table_path} TO 100 PERCENT",
                    do_print=do_print,
                )
            except vacuum_errors:
                LOG.info('INFO: unable to vacuum "%s"', table_name)

    def __del__(self, *args: Any) -> None:
        LOG.info("INFO: worker down at %s.", datetime.utcnow())
        LOG.info("INFO: %s seconds elapsed.", time.time() - self.initt)
