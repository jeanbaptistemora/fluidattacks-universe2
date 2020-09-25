"""Process Redshift data and compute bills for every namespace."""

# Standard library
import argparse
import csv
from datetime import (
    datetime,
)
import json
from operator import (
    itemgetter,
)
import os
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
)

# Local libraries
from shared import (
    COMMIT_HASH_SENTINEL,
    db_cursor,
    log_sync,
)

# Constants
SELECT_ALL: str = """
    SELECT
        author_name || ' <' || author_email || '>' AS "actor",
        hash,
        namespace,
        repository
    FROM code.commits
    WHERE
        TO_CHAR(seen_at, 'YYYY-MM') = %(seen_at)s
        AND hash != %(hash)s
"""

# Types
MonthData = Dict[str, Dict[str, List[Any]]]


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True)
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    args = parser.parse_args()

    data, groups = get_date_data(args.year, args.month)

    for group in groups:
        log_sync('info', 'Creating bill for: %s', group)
        create_csv_file(args.folder, data, group)


def get_date_data(year: int, month: int) -> Tuple[MonthData, Set[str]]:
    """Return a dictionary mapping actors to namespaces to lists of commits.

    Return a set of namespaces as well.
    """
    data: MonthData = {}
    groups = set()

    date: str = datetime(year, month, 1).strftime('%Y-%m')

    log_sync('info', 'Computing bills for date: %s', date)

    with db_cursor() as cursor:
        cursor.execute(SELECT_ALL, dict(
            hash=COMMIT_HASH_SENTINEL,
            seen_at=date,
        ))
        for row in cursor:
            row = dict(zip(map(itemgetter(0), cursor.description), row))

            actor = row.pop('actor')
            group = row.pop('namespace')

            data.setdefault(actor, {})
            data[actor].setdefault(group, [])
            data[actor][group].append(row)
            groups.add(group)

    log_sync('info', 'Data: %s', json.dumps(data, indent=2))

    return data, groups


def create_csv_file(folder: str, data: MonthData, group: str) -> None:
    with open(os.path.join(folder, f'{group}.csv'), 'w') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=(
                'actor',
                'groups',
                '# groups',
                'commit',
                'repository',
            ),
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()

        for actor, actor_groups in data.items():
            if group in actor_groups:
                groups_contributed = actor_groups
                writer.writerow({
                    'actor': actor,
                    'groups': ', '.join(groups_contributed),
                    '# groups': len(groups_contributed),
                    'commit': actor_groups[group][-1]['hash'],
                    'repository': actor_groups[group][-1]['repository'],
                })


if __name__ == '__main__':
    cli()
