"""Process Redshift data and compute bills for every namespace."""


import argparse
from code_etl.compute_bills._getter import (
    get_org as get_organization,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
    db_cursor,
)
import csv
from datetime import (
    datetime,
)
import json
import logging
from operator import (
    itemgetter,
)
import os
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
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

LOG = logging.getLogger(__name__)

# Types
MonthData = Dict[str, Dict[str, List[Any]]]


def get_date_data(year: int, month: int) -> Tuple[MonthData, Set[str]]:
    """Return a dictionary mapping actors to namespaces to lists of commits.

    Return a set of namespaces as well.
    """
    data: MonthData = {}
    groups = set()

    date: str = datetime(year, month, 1).strftime("%Y-%m")

    LOG.info("Computing bills for date: %s", date)

    with db_cursor() as cursor:
        cursor.execute(
            SELECT_ALL,
            dict(
                hash=COMMIT_HASH_SENTINEL,
                seen_at=date,
            ),
        )
        for row in cursor:
            _row = dict(zip(map(itemgetter(0), cursor.description), row))

            actor = _row.pop("actor")
            group = _row.pop("namespace")

            data.setdefault(actor, {})
            data[actor].setdefault(group, [])
            data[actor][group].append(_row)
            groups.add(group)

    LOG.info("Data: %s", json.dumps(data, indent=2))

    return data, groups


def groups_of_org(
    org: str, groups: Iterable[str], get_org: Callable[[str], Optional[str]]
) -> Set[str]:
    return set(filter(lambda group: get_org(group) == org, groups))


def create_csv_file(
    folder: str,
    data: MonthData,
    group: str,
    get_org: Callable[[str], Optional[str]],
) -> None:
    with open(
        os.path.join(folder, f"{group}.csv"), "w", encoding="UTF-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=(
                "actor",
                "groups",
                "commit",
                "repository",
            ),
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()

        for actor, actor_groups in data.items():
            if group in actor_groups:
                org = get_org(group)
                if org:
                    groups_contributed = groups_of_org(
                        org, actor_groups, get_org
                    )
                    writer.writerow(
                        {
                            "actor": actor,
                            "groups": ", ".join(groups_contributed),
                            "commit": actor_groups[group][-1]["hash"],
                            "repository": actor_groups[group][-1][
                                "repository"
                            ],
                        }
                    )
                else:
                    LOG.warning("Skipped group contribution: %s", group)


def main(folder: str, year: int, month: int, integrates_token: str) -> None:
    data, groups = get_date_data(year, month)
    for group in groups:
        LOG.info("Creating bill for: %s", group)
        create_csv_file(
            folder,
            data,
            group,
            lambda i: get_organization(integrates_token, i),
        )


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    parser.add_argument("--integrates-token", type=str, required=True)

    args = parser.parse_args()
    main(args.folder, args.year, args.month, args.integrates_token)


if __name__ == "__main__":
    cli()
