# pylint: skip-file

from code_etl.client.decoder import (
    decode_commit_data,
    RawDecodeError,
)
from code_etl.factories import (
    gen_fa_hash,
)
from code_etl.objs import (
    CommitData,
    CommitDataId,
    CommitId,
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
    PureIter,
)
from purity.v1.pure_iter.factory import (
    pure_map,
)
from purity.v1.pure_iter.transform import (
    filter_maybe,
)
from returns.functions import (
    raise_exception,
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


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise TypeError("Not a str obj")


def _assert_int(raw: Any) -> int:
    if isinstance(raw, int):
        return raw
    raise TypeError("Not a int obj")


def calc_commit_id(
    data: CommitData, namespace: str, repository: str, hash: str
) -> CommitDataId:
    return CommitDataId(
        namespace, repository, CommitId(hash, gen_fa_hash(data))
    )


def _calc_id(raw: FrozenList[Any]) -> CommitDataId:
    try:
        data = decode_commit_data(raw).alt(raise_exception).unwrap()
        _id = calc_commit_id(
            data,
            _assert_str(raw[12]),
            _assert_str(raw[13]),
            _assert_str(raw[14]),
        )
        return _id
    except TypeError as err:
        raise RawDecodeError("CommitDataId", raw) from err
    except KeyError as err:
        raise RawDecodeError("CommitDataId", raw) from err


def _try_calc_id(raw: FrozenList[Any]) -> Maybe[CommitDataId]:
    _raw = Maybe.from_optional(raw if raw[0] is not None else None)
    return _raw.map(_calc_id)


def update_query(schema: SchemaID) -> Query:
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
            identifiers={"schema": schema.name},
        ),
    )


def calc_hash(
    client: Client, client_2: Client, schema: SchemaID, namespace: str
) -> IO[None]:
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
        data: PureIter[CommitDataId] = filter_maybe(
            pure_map(_try_calc_id, items)
        )
        args = data.map(
            lambda cid: SqlArgs(
                {
                    "fa_hash": cid.hash.fa_hash,
                    "hash": cid.hash.hash,
                    "namespace": cid.namespace,
                    "repository": cid.repository,
                }
            )
        )
        LOG.info("%s items will be updated", len(tuple(data)))
        client_2.cursor.execute_batch(update_query(schema), list(args))
        count = count + len(items)
        LOG.info(
            "Migration %s/%s [%s%%]", count, total, (count * 100) // total
        )
        if len(items) == 0:
            LOG.info("END. No more packages")
            break
    return IO(None)


def start(
    db_id: DatabaseID, creds: Credentials, schema: SchemaID, namespace: str
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    client2 = ClientFactory().from_creds(db_id, creds)
    return calc_hash(client, client2, schema, namespace)
