# Standard library
import csv
from operator import itemgetter
import sys

# Local libraries
from toolbox.utils import postgres


def create():
    with postgres.database() as (_, cursor):
        fieldnames = postgres.get_columns(cursor, 'code', 'commits')
        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        cursor.execute("""
            SELECT * FROM code.commits
            WHERE TO_CHAR(authored_at, 'YYYY-MM')
                = TO_CHAR(SYSDATE, 'YYYY-MM')
            """)

        for row in cursor:
            result = dict(zip(map(itemgetter(0), cursor.description), row))
            writer.writerow(result)
    return True
