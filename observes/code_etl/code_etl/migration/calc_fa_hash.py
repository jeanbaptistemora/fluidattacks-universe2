from code_etl.factories import (
    gen_fa_hash,
)
from code_etl.objs import (
    CommitData,
    CommitDataId,
    CommitId,
    Deltas,
    User,
)
from datetime import (
    datetime,
)
from postgres_client.client import (
    Client,
    ClientFactory,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.ids import (
    SchemaID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from purity.v1 import (
    FrozenList,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Any,
)


class RawDecodeError(Exception):
    def __init__(
        self,
        target: str,
        raw: Any,
    ):
        super().__init__(
            f"TypeError when trying to build `{target}` "
            f"from raw obj `{str(raw)}`"
        )


def _calc_id(raw: FrozenList[Any]) -> CommitDataId:
    try:
        data = CommitData(
            User(raw[0], raw[1]),
            datetime.fromisoformat(raw[2]),
            User(raw[3], raw[4]),
            datetime.fromisoformat(raw[5]),
            raw[6],
            raw[7],
            Deltas(raw[8], raw[9], raw[10], raw[11]),
        )
        _id = CommitDataId(
            raw[11], raw[12], CommitId(raw[13], gen_fa_hash(data))
        )
        return _id
    except TypeError as err:
        raise RawDecodeError("CommitId", raw) from err


def _try_calc_id(raw: FrozenList[Any]) -> Maybe[CommitDataId]:
    _raw = Maybe.from_optional(raw if raw[0] is not None else None)
    return _raw.map(_calc_id)


def update_query(schema: SchemaID, cid: CommitDataId) -> Query:
    return Query(
        """
        UPDATE {schema}.commits
        SET
            fa_hash = %(fa_hash)s
        WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
        """,
        SqlArgs(
            {
                "fa_hash": cid.hash.fa_hash,
                "hash": cid.hash.hash,
                "namespace": cid.namespace,
                "repository": cid.repository,
            },
            {"schema": schema.name},
        ),
    )


def calc_hash(client: Client, schema: SchemaID, namespace: str) -> IO[None]:
    query = Query(
        """
        SELECT
            author_name,
            author_email,
            authored_at,
            committer_email,
            committer_name,
            committed_at,
            message,
            summary,
            total_insertions,
            total_deletions,
            total_lines,
            total_files,
            namespace,
            repository,
            hash
        FROM {schema}.commits WHERE
            fa_hash IS NULL
            and namespace = %(namespace)s
        """,
        SqlArgs({"namespace": namespace}, {"schema": schema.name}),
    )
    client.cursor.execute_query(query)
    while True:
        items = unsafe_perform_io(client.cursor.fetch_many(2000))
        for item in items:
            _try_calc_id(item).map(
                lambda c: client.cursor.execute_query(update_query(schema, c))
            )
        if len(items) == 0:
            break
    return IO(None)


def start(
    db_id: DatabaseID, creds: Credentials, schema: SchemaID, namespace: str
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    return calc_hash(client, schema, namespace)
