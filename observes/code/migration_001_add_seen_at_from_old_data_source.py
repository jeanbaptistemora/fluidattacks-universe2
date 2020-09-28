# Local libraries
from shared import (
    db_cursor,
    log_sync,
)


def main() -> None:
    with db_cursor() as cursor_old, db_cursor() as cursor:
        cursor_old.execute(
            """ SELECT
                    authored_at,
                    hash,
                    namespace,
                    repository
                FROM code.commits
                WHERE (
                    seen_at < '2020-01-01'
                    AND authored_at >= '2020-01-01'
                    AND authored_at < '2020-08-01'
                )
            """
        )
        for (
            authored_at,
            commit_hash,
            namespace,
            repository,
        ) in cursor_old:
            query = cursor.mogrify(
                """
                UPDATE code.commits
                SET seen_at = %(seen_at)s
                WHERE
                    hash = %(hash)s
                    AND namespace = %(namespace)s
                    AND repository = %(repository)s
                """,
                dict(
                    hash=commit_hash,
                    seen_at=authored_at,
                    namespace=namespace,
                    repository=repository,
                )
            ).decode()
            log_sync('info', 'executing: %s', query)
            cursor.execute(query)


if __name__ == '__main__':
    main()
