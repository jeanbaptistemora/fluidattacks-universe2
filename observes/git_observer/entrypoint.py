# Standard library
from asyncio import (
    Queue,
)
from contextlib import (
    contextmanager,
)
from datetime import (
    datetime,
)
import logging
from os import (
    environ,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
from psycopg2 import (
    connect,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from psycopg2.extras import (
    execute_batch,
)

# Constants
CHECK_INTERVAL: int = 1024
COMMIT_HASH_SENTINEL: str = '-' * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()
INSERT_QUERY = """
    INSERT INTO code.commits (
        author_email, author_name, authored_at,
        committer_email, committer_name, committed_at,
        hash, message, summary,
        total_insertions, total_deletions,
        total_lines, total_files,

        seen_at, namespace, repository
    )
    VALUES (
        %(author_email)s, %(author_name)s, %(authored_at)s,
        %(committer_email)s, %(committer_name)s, %(committed_at)s,
        %(hash)s, %(message)s, %(summary)s,
        %(total_insertions)s, %(total_deletions)s,
        %(total_lines)s, %(total_files)s,

        %(seen_at)s, %(namespace)s, %(repository)s
    )
"""
WORKERS_COUNT: int = 16
WORKERS_PAGE_SIZE: int = 1024

# Logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.addHandler(logging.StreamHandler())
LOG.handlers[0].setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(getattr(LOG, level), msg, *args)


async def worker(identifier: int, queue: Queue) -> None:
    with db_cursor() as cursor:
        while True:
            items = await drain_queue(queue)

            await log('info', 'Worker[%s]: Sending %s', identifier, len(items))
            await in_thread(
                execute_batch,
                cur=cursor,
                sql=INSERT_QUERY,
                argslist=items,
                page_size=WORKERS_PAGE_SIZE,
            )

            for _ in items:
                queue.task_done()


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = connect(
        dbname=environ['REDSHIFT_DATABASE'],
        host=environ['REDSHIFT_HOST'],
        password=environ['REDSHIFT_PASSWORD'],
        port=environ['REDSHIFT_PORT'],
        user=environ['REDSHIFT_USER'],
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


async def register_repository(
    cursor: cursor_cls,
    namespace: str,
    repository: str,
) -> None:
    await log('info', 'Registering: %s/%s', namespace, repository)
    await in_thread(
        cursor.execute,
        """
            INSERT INTO code.commits (hash, seen_at, namespace, repository)
            VALUES (%(hash)s, %(seen_at)s, %(namespace)s, %(repository)s)
        """,
        dict(
            hash=COMMIT_HASH_SENTINEL,
            seen_at=DATE_NOW,
            namespace=namespace,
            repository=repository,
        ),
    )


async def drain_queue(queue: Queue) -> List[Dict[str, Any]]:
    items = [await queue.get()]
    items_to_get = min(WORKERS_PAGE_SIZE - 1, queue.qsize())
    items.extend(queue.get_nowait() for _ in range(items_to_get))
    return items
