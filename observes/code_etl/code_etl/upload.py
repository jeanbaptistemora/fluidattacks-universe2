"""Process repositories and upload their data to Redshift."""


from aioextensions import (
    generate_in_thread,
    in_thread,
    run,
)
import argparse
from asyncio import (
    create_task,
    Queue,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
    DATE_NOW,
    DATE_SENTINEL,
    db_cursor,
    log,
)
from contextlib import (
    suppress,
)
from git import (
    GitCommandError,
    InvalidGitRepositoryError,
    Repo,
)
from git.objects import (
    Commit,
)
from os.path import (
    abspath,
    basename,
)
from psycopg2.errors import (
    DuplicateTable,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from psycopg2.extras import (
    execute_batch,
)
import sys
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
)

# Constants
INSERT_QUERY = """
    INSERT INTO code.commits (
        author_email, author_name, authored_at,
        committer_email, committer_name, committed_at,
        hash, message, summary,
        total_insertions, total_deletions,
        total_lines, total_files,

        namespace, repository, seen_at
    )
    SELECT
        %(author_email)s, %(author_name)s, %(authored_at)s,
        %(committer_email)s, %(committer_name)s, %(committed_at)s,
        %(hash)s, %(message)s, %(summary)s,
        %(total_insertions)s, %(total_deletions)s,
        %(total_lines)s, %(total_files)s,

        %(namespace)s, %(repository)s, %(seen_at)s
    WHERE NOT EXISTS (
        SELECT hash, namespace, repository
        FROM code.commits
        WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
    )
"""
WORKERS_COUNT: int = 8
WORKERS_PAGE_SIZE: int = 1024


async def worker(identifier: int, queue: Queue) -> None:
    with db_cursor() as cursor:
        while True:
            items = await drain_queue(queue)

            await log("info", "Worker[%s]: Sending %s", identifier, len(items))
            await in_thread(
                execute_batch,
                cur=cursor,
                sql=INSERT_QUERY,
                argslist=items,
                page_size=WORKERS_PAGE_SIZE,
            )

            for _ in items:
                queue.task_done()


async def main(namespace: str, *repositories: str) -> bool:
    await initialize()

    queue: Queue = Queue(maxsize=2 * WORKERS_PAGE_SIZE * WORKERS_COUNT)
    worker_tasks = [
        create_task(worker(identifier, queue))
        for identifier in range(WORKERS_COUNT)
    ]

    success: bool = await manager(queue, namespace, *repositories)

    await queue.join()

    for worker_task in worker_tasks:
        worker_task.cancel()

    return success


def truncate_bytes(string: str, start: int, end: int) -> str:
    return string.encode()[start:end].decode()


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", required=True)
    parser.add_argument("repositories", nargs="*")
    args = parser.parse_args()

    repositories: Iterator[str] = map(abspath, args.repositories)

    success: bool = run(main(args.namespace, *repositories))

    sys.exit(0 if success else 1)


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
        total_insertions=commit.stats.total["insertions"],
        total_deletions=commit.stats.total["deletions"],
        total_lines=commit.stats.total["lines"],
        total_files=commit.stats.total["files"],
    )


async def manager(queue: Queue, namespace: str, *repositories: str) -> bool:
    commit: Commit
    success: bool = True
    with db_cursor() as cursor:
        for repo_path in repositories:
            repo_name: str = basename(repo_path)
            repo_is_new: bool = not await does_commit_exist(
                cursor,
                COMMIT_HASH_SENTINEL,
                namespace,
                repo_name,
            )
            repo_last_commit: Optional[str] = await get_last_commit(
                cursor,
                namespace,
                repo_name,
            )

            try:
                repo_obj: Repo = Repo(repo_path)
                async for commit in generate_in_thread(
                    repo_obj.iter_commits,
                    no_merges=True,
                    topo_order=True,
                ):
                    if commit.hexsha == repo_last_commit:
                        break

                    await queue.put(
                        dict(
                            namespace=namespace,
                            repository=repo_name,
                            seen_at=DATE_SENTINEL if repo_is_new else DATE_NOW,
                            **get_commit_data(commit),
                        )
                    )
            except ValueError:
                await log("error", "Repository is possibly empty, ignoring")
                success = False
            except (GitCommandError, InvalidGitRepositoryError):
                await log("error", "Invalid or corrupt repository")
                success = False

            if repo_is_new:
                await queue.join()
                await register_repository(cursor, namespace, repo_name)

    return success


async def does_commit_exist(
    cursor: cursor_cls,
    commit_hash: str,
    namespace: str,
    repository: str,
) -> bool:
    """Return True if the repository is new for the provided namespace."""
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


async def get_last_commit(
    cursor: cursor_cls,
    namespace: str,
    repository: str,
) -> Optional[str]:
    """Return the last seen commit for the provided namespace/repository."""
    await in_thread(
        cursor.execute,
        """
            SELECT hash
            FROM code.commits
            WHERE
                hash != %(sentinel)s
                and namespace = %(namespace)s
                and repository = %(repository)s
            ORDER BY seen_at DESC, authored_at DESC
            LIMIT 1
        """,
        dict(
            sentinel=COMMIT_HASH_SENTINEL,
            namespace=namespace,
            repository=repository,
        ),
    )

    # The list has values if the item exists
    data = await in_thread(cursor.fetchall)
    if data and data[0]:
        return data[0][0]
    return None


async def register_repository(
    cursor: cursor_cls,
    namespace: str,
    repository: str,
) -> None:
    await log("info", "Registering: %s/%s", namespace, repository)
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
            await log("info", "Ensuring code.commits table exists...")
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

                        namespace VARCHAR(64),
                        repository VARCHAR(4096),
                        seen_at TIMESTAMPTZ,

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


if __name__ == "__main__":
    cli()
