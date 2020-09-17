# Standard library
import csv
from operator import itemgetter
import sys

# Local libraries
from toolbox.utils import postgres


def create():
    with postgres.database() as (_, cursor):
        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=postgres.get_columns(cursor, 'git', 'commits'),
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()

        cursor.execute("""
            SELECT * FROM git.commits
            WHERE TO_CHAR(integration_authored_at, 'YYYY-MM')
                = TO_CHAR(SYSDATE, 'YYYY-MM')
            """)

        for row in cursor:
            writer.writerow(
                dict(zip(map(itemgetter(0), cursor.description), row))
            )
    return True
