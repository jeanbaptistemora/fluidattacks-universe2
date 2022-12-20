from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class RepoId:
    group: str
    name: str


@dataclass(frozen=True)
class Query:
    query_info: str
    values: dict[str, str]


def insert(repo: RepoId) -> Query:
    query = (
        "INSERT INTO last_update.repos "
        '("group", repo, updated_at) VALUES (%(group)s, %(repo)s, getdate())'
    )
    return Query(query, {"group": repo.group, "repo": repo.name})


def update(repo: RepoId) -> Query:
    query = (
        "UPDATE last_update.repos "
        'set updated_at=getdate() WHERE "group"=%(group)s AND repo=%(repo)s'
    )
    return Query(query, {"group": repo.group, "repo": repo.name})


def get(repo: RepoId) -> Query:
    query = (
        "SELECT * FROM last_update.repos "
        'WHERE "group"=%(group)s AND repo=%(repo)s'
    )
    return Query(query, {"group": repo.group, "repo": repo.name})
