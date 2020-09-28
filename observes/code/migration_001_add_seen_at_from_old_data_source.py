# Local libraries
from shared import (
    db_cursor,
    log_sync,
)


def main() -> None:
    with db_cursor() as cursor_old, db_cursor() as cursor:
        cursor_old.execute(
            """ SELECT
                    integration_authored_at,
                    sha1,
                    subscription,
                    repository
                FROM git.commits
                WHERE (
                    (integration_authored_at AT TIME ZONE 'UTC') < '2020-08-01'
                )
            """
        )
        for (
            integration_authored_at,
            sha1,
            subscription,
            repository,
        ) in cursor_old:
            query = cursor.mogrify(
                """
                UPDATE code.commits
                SET
                    seen_at = %(seen_at)s
                WHERE
                    hash = %(hash)s
                    and namespace = %(namespace)s
                    and repository = %(repository)s
                """,
                dict(
                    hash=sha1,
                    seen_at=integration_authored_at,
                    namespace=subscription,
                    repository=repository,
                )
            ).decode()
            log_sync('info', 'executing: %s', query)
            cursor.execute(query)


if __name__ == '__main__':
    main()
