"""Functions to connect to the analytics database."""


import sys
from contextlib import contextmanager

import rollbar
import psycopg2

from __init__ import (
    FI_AWS_REDSHIFT_DB_NAME, FI_AWS_REDSHIFT_USER, FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_HOST, FI_AWS_REDSHIFT_PORT
)


def redshift_conection():
    """Connect to the redshift database."""
    connection = psycopg2.connect(user=FI_AWS_REDSHIFT_USER,
                                  password=FI_AWS_REDSHIFT_PASSWORD,
                                  host=FI_AWS_REDSHIFT_HOST,
                                  port=FI_AWS_REDSHIFT_PORT,
                                  dbname=FI_AWS_REDSHIFT_DB_NAME)
    return connection


@contextmanager
def query():
    """Query in the redshift database."""
    connection = ''
    try:
        connection = redshift_conection()
        cursor = connection.cursor()
        yield (cursor, connection)
    except psycopg2.DatabaseError:
        rollbar.report_exc_info(sys.exc_info())
    finally:
        if connection:
            cursor.close()
            connection.close()
