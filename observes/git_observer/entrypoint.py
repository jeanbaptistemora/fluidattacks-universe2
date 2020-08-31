# Standard library
import argparse
from asyncio import (
    create_task,
    Queue,
)
from contextlib import (
    contextmanager,
    suppress,
)
from datetime import (
    datetime,
)
import logging
from os import (
    environ,
)
from os.path import (
    abspath,
    basename,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
)

# Third party libraries
from aioextensions import (
    generate_in_thread,
    in_thread,
    run,
)
from psycopg2 import (
    connect,
)
from psycopg2.errors import (
    DuplicateTable,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from psycopg2.extras import (
    execute_batch,
)
from git import (
    Commit,
    Repo,
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


async def main(namespace: str, *repositories: str) -> None:
    await initialize()

    queue: Queue = Queue(maxsize=2 * WORKERS_PAGE_SIZE * WORKERS_COUNT)
    worker_tasks = [
        create_task(worker(identifier, queue))
        for identifier in range(WORKERS_COUNT)
    ]

    await manager(queue, namespace, *repositories)
    await queue.join()

    for worker_task in worker_tasks:
        worker_task.cancel()


def truncate_bytes(string: str, start: int, end: int) -> str:
    return string.encode()[start:end].decode()


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--namespace', required=True)
    parser.add_argument('repositories', nargs='+')
    args = parser.parse_args()

    repositories: Iterator[str] = map(abspath, args.repositories)

    run(main(args.namespace, *repositories))


def get_commit_data(commit: Commit) -> Dict[str, Any]:
    return dict(
        author_email=truncate_bytes(commit.author.email, 0, 256),
        author_name=truncate_bytes(commit.author.name, 0, 256),
        authored_at=commit.authored_datetime,
        committer_email=truncate_bytes(commit.committer.email, 0, 256),
        committer_name=truncate_bytes(commit.committer.name, 0, 256),
        committed_at=commit.committed_datetime,
        hash=commit.hexsha,
        message=truncate_bytes(commit.message, 0, 4096),
        summary=truncate_bytes(commit.summary, 0, 256),
        total_insertions=commit.stats.total['insertions'],
        total_deletions=commit.stats.total['deletions'],
        total_lines=commit.stats.total['lines'],
        total_files=commit.stats.total['files'],
    )


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


async def manager(queue: Queue, namespace: str, *repositories: str) -> None:
    counter = CHECK_INTERVAL
    commit: Commit
    with db_cursor() as cursor:
        for repo_path in repositories:
            repo_obj: Repo = Repo(repo_path)
            repo_name: str = basename(repo_path)
            repo_is_new: bool = not await does_commit_exist(
                cursor, COMMIT_HASH_SENTINEL, namespace, repo_name,
            )

            async for commit in generate_in_thread(repo_obj.iter_commits):
                # Every # commits let's check if we've already walked this
                if counter % CHECK_INTERVAL == 0:
                    if await does_commit_exist(
                        cursor, commit.hexsha, namespace, repo_name,
                    ):
                        break

                await queue.put(dict(
                    namespace=namespace,
                    repository=repo_name,
                    seen_at=DATE_SENTINEL if repo_is_new else DATE_NOW,
                    **get_commit_data(commit),
                ))

                counter += 1

            if repo_is_new:
                await queue.join()
                await register_repository(cursor, namespace, repo_name)


async def does_commit_exist(
    cursor: cursor_cls,
    commit_hash: str,
    namespace: str,
    repository: str,
) -> bool:
    """Return True if the repository is new for the provided namespace.
    """
    await in_thread(
        cursor.execute,
        """
            SELECT hash, namespace, repository
            FROM code.commits
            WHERE
                hash = %(commit_hash)s
                and namespace = %(namespace)s
                and repository = %(repository)s
        """,
        dict(
            commit_hash=commit_hash,
            namespace=namespace,
            repository=repository,
        ),
    )

    # The list has values if the item exists
    return bool(await in_thread(cursor.fetchall))


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


async def initialize() -> None:
    with db_cursor() as cursor:
        # Initialize the table if not done yet
        with suppress(DuplicateTable):
            await log('info', 'Ensuring code.commits table exists...')
            await in_thread(
                cursor.execute,
                """
                    CREATE TABLE code.commits (
                        author_email VARCHAR(256),
                        author_name VARCHAR(256),
                        authored_at TIMESTAMPTZ,
                        committer_email VARCHAR(256),
                        committer_name VARCHAR(256),
                        committed_at TIMESTAMPTZ,
                        hash VARCHAR(40),
                        message VARCHAR(4096),
                        summary VARCHAR(256),
                        total_insertions INTEGER,
                        total_deletions INTEGER,
                        total_lines INTEGER,
                        total_files INTEGER,

                        seen_at TIMESTAMPTZ,
                        namespace VARCHAR(64),
                        repository VARCHAR(4096),

                        PRIMARY KEY (
                            namespace,
                            repository,
                            hash
                        )
                    )
                """,
            )


async def drain_queue(queue: Queue) -> List[Dict[str, Any]]:
    items = [await queue.get()]
    items_to_get = min(WORKERS_PAGE_SIZE - 1, queue.qsize())
    items.extend(queue.get_nowait() for _ in range(items_to_get))
    return items


if __name__ == '__main__':
    cli()
