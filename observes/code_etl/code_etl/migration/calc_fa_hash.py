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
import logging
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

LOG = logging.getLogger(__name__)


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


def _assert_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise TypeError("Not a datetime obj")


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise TypeError("Not a str obj")


def _assert_int(raw: Any) -> int:
    if isinstance(raw, int):
        return raw
    raise TypeError("Not a int obj")


def _calc_id(raw: FrozenList[Any]) -> CommitDataId:
    try:
        data = CommitData(
            User(_assert_str(raw[0]), _assert_str(raw[1])),
            _assert_datetime(raw[2]),
            User(_assert_str(raw[3]), _assert_str(raw[4])),
            _assert_datetime(raw[5]),
            _assert_str(raw[6]),
            _assert_str(raw[7]),
            Deltas(
                _assert_int(raw[8]),
                _assert_int(raw[9]),
                _assert_int(raw[10]),
                _assert_int(raw[11]),
            ),
        )
        _id = CommitDataId(
            _assert_str(raw[12]),
            _assert_str(raw[13]),
            CommitId(_assert_str(raw[14]), gen_fa_hash(data)),
        )
        return _id
    except TypeError as err:
        raise RawDecodeError("CommitId", raw) from err


def _try_calc_id(raw: FrozenList[Any]) -> Maybe[CommitDataId]:
    _raw = Maybe.from_optional(raw if raw[0] is not None else None)
    return _raw.map(_calc_id)


def update_query(schema: SchemaID, cid: CommitDataId) -> Query:
    LOG.debug("updating commit %s", cid.hash.hash)
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
    total_query = Query(
        """
        SELECT COUNT(*)
        FROM {schema}.commits WHERE
            fa_hash IS NULL
            and namespace = %(namespace)s
        """,
        SqlArgs({"namespace": namespace}, {"schema": schema.name}),
    )
    client.cursor.execute_query(total_query)
    pkg_items = 2000
    total = _assert_int(unsafe_perform_io(client.cursor.fetch_one())[0])
    client.cursor.execute_query(query)
    count = 0
    while True:
        if total == 0:
            LOG.info("No items")
            break
        items = unsafe_perform_io(client.cursor.fetch_many(pkg_items))
        for item in items:
            _try_calc_id(item).map(
                lambda c: client.cursor.execute_query(update_query(schema, c))
            )
            count = count + 1
            LOG.info(
                "migrating %s/%s [%s%%]", count, total, (count * 100) // total
            )
        if len(items) == 0:
            LOG.info("END. No more packages")
            break
    return IO(None)


def start(
    db_id: DatabaseID, creds: Credentials, schema: SchemaID, namespace: str
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    return calc_hash(client, schema, namespace)
