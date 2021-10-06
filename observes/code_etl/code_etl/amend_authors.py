"""Walks all data in Redshift and edit those authors accordingly to mailmap."""


from aioextensions import (
    generate_in_thread,
    in_thread,
)
import argparse
from asyncio import (
    create_task,
    Queue,
    run,
)
from code_etl.utils import (
    db_cursor,
    log,
)
import re
from typing import (
    Dict,
    List,
    Match,
    NamedTuple,
    Optional,
    Pattern,
    Tuple,
)

# Constants
WORKERS_COUNT: int = 8
MailmapMapping = Dict[Tuple[str, str], Tuple[str, str]]
"""Mapping from (author, email) to (canonical_author, canonical_email)."""
UPDATE_QUERY: str = """
    UPDATE code.commits
    SET
        author_email = %(author_email)s,
        author_name = %(author_name)s,
        committer_email = %(committer_email)s,
        committer_name = %(committer_name)s
    WHERE
        hash = %(hash)s
        and namespace = %(namespace)s
        and repository = %(repository)s
"""


class Item(NamedTuple):
    hash: str
    namespace: str
    repository: str
    author_email: str
    author_name: str
    committer_email: str
    committer_name: str


def get_mailmap_dict(mailmap_path: str) -> MailmapMapping:
    # This format is guaranteed by:
    #   https://github.com/kamadorueda/mailmap-linter
    #     /blob/5ae9d2654375afb76dfb3087b1e9b200257331a2/default.nix#L39
    mailmap_dict: MailmapMapping = {}
    mailmap_line: Pattern = re.compile(
        r"^(?P<canon_name>[A-Z][a-z]+ [A-Z][a-z]+) "
        r"<(?P<canon_email>.*)> "
        r"(?P<name>.*?) "
        r"<(?P<email>.*?)>$",
    )

    with open(mailmap_path, encoding="UTF-8") as file:
        for line in file.read().splitlines():
            match: Optional[Match] = mailmap_line.match(line)
            if match:
                mapping = match.groupdict()
                mailmap_from = (mapping["name"], mapping["email"])
                mailmap_to = (mapping["canon_name"], mapping["canon_email"])
                if mailmap_from != mailmap_to:
                    mailmap_dict[mailmap_from] = mailmap_to

    return mailmap_dict


async def get_items_to_change(
    items: List[Item],
    mailmap_dict: MailmapMapping,
) -> List[Item]:
    items_to_change = []
    for item in items:
        item_data = item._asdict()
        author = (item.author_name, item.author_email)
        author_fixed = mailmap_dict.get(author)

        if author_fixed:
            await log(
                "warning",
                "Update author from: %s, to: %s",
                author,
                author_fixed,
            )
            item_data["author_name"] = author_fixed[0]
            item_data["author_email"] = author_fixed[1]

        committer = (item.committer_name, item.committer_email)
        committer_fixed = mailmap_dict.get(committer)

        if committer_fixed:
            await log(
                "warning",
                "Update committer from: %s, to: %s",
                committer,
                committer_fixed,
            )
            item_data["committer_name"] = committer_fixed[0]
            item_data["committer_email"] = committer_fixed[1]

        if author_fixed or committer_fixed:
            items_to_change.append(Item(**item_data))

    return items_to_change


async def worker(
    identifier: int,
    queue: Queue,
    mailmap_dict: MailmapMapping,
) -> None:
    with db_cursor() as cursor:
        while True:
            item: Item = await queue.get()
            items_to_change = await get_items_to_change([item], mailmap_dict)

            for item in items_to_change:
                await log(
                    "info",
                    "Worker[%s]: Sending to %s",
                    identifier,
                    item.namespace,
                )
                await in_thread(cursor.execute, UPDATE_QUERY, item._asdict())

            queue.task_done()


async def item_emitter(queue: Queue) -> None:
    # Iterate all rows in the DB and put them on a queue
    with db_cursor() as cursor:
        cursor.itersize = 100
        await in_thread(
            cursor.execute,
            """ SELECT
                    hash, namespace, repository,
                    author_email, author_name,
                    committer_email, committer_name
                FROM code.commits
                ORDER BY namespace
            """,
        )
        async for (
            commit_hash,
            namespace,
            repository,
            author_email,
            author_name,
            committer_email,
            committer_name,
        ) in generate_in_thread(lambda: cursor):
            await queue.put(
                Item(
                    hash=commit_hash,
                    namespace=namespace,
                    repository=repository,
                    author_email=author_email,
                    author_name=author_name,
                    committer_email=committer_email,
                    committer_name=committer_name,
                )
            )


async def main(mailmap_path: str) -> None:
    mailmap_dict: MailmapMapping = get_mailmap_dict(mailmap_path)
    queue: Queue = Queue(maxsize=2 * WORKERS_COUNT)
    worker_tasks = [
        create_task(worker(identifier, queue, mailmap_dict))
        for identifier in range(WORKERS_COUNT)
    ]

    await item_emitter(queue)
    await queue.join()

    for worker_task in worker_tasks:
        worker_task.cancel()


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mailmap-path", required=True)

    args = parser.parse_args()

    run(main(args.mailmap_path))


if __name__ == "__main__":
    cli()
