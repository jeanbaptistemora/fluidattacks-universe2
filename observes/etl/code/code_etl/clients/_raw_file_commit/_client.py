from . import (
    _decode,
    _encode,
)
from code_etl.clients._raw_objs import (
    RawFileCommitRelation,
)
from code_etl.objs import (
    CommitDataId,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    Dict,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class RawFileCommitClient:
    _sql_client: SqlClient
    _table: TableId

    def insert(self, rows: FrozenList[RawFileCommitRelation]) -> Cmd[None]:
        _fields = ",".join(RawFileCommitRelation.fields())
        values = ",".join(
            tuple(f"%({f})s" for f in RawFileCommitRelation.fields())
        )
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        query = Query.dynamic_query(
            f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values})",
            freeze(identifiers),
        )
        msg = Cmd.from_cmd(lambda: LOG.debug("inserting %s rows", len(rows)))
        return msg.bind(
            lambda _: self._sql_client.batch(
                query,
                tuple(QueryValues(_encode.primitive_encode(r)) for r in rows),
            )
        )

    def get(
        self, id_obj: CommitDataId
    ) -> Cmd[FrozenList[RawFileCommitRelation]]:
        statement = """
            SELECT file_path FROM {schema}.{table} WHERE
                hash = %(hash)s
                and namespace = %(namespace)s
                and repository = %(repository)s
        """
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        values: Dict[str, PrimitiveVal] = {
            "hash": id_obj.hash.hash,
            "namespace": id_obj.repo.namespace,
            "repository": id_obj.repo.repository,
        }
        query = Query.dynamic_query(statement, freeze(identifiers))
        msg = Cmd.from_cmd(
            lambda: LOG.debug("getting commit files  of %s", id_obj)
        )
        files = msg.bind(
            lambda _: self._sql_client.execute(
                query,
                QueryValues(freeze(values)),
            )
            + self._sql_client.fetch_all().map(
                lambda x: tuple(
                    _decode.decode_file_path(i).alt(raise_exception).unwrap()
                    for i in x
                )
            )
        )

        def _build_relation(file: str) -> RawFileCommitRelation:
            return RawFileCommitRelation(
                id_obj.hash.hash,
                id_obj.repo.namespace,
                id_obj.repo.repository,
                file,
            )

        return files.map(lambda f: tuple(_build_relation(i) for i in f))

    def has_files(self, id_obj: CommitDataId) -> Cmd[bool]:
        statement = """
        SELECT EXISTS (
            SELECT 1 FROM {schema}.{table} WHERE
                hash = %(hash)s
                and namespace = %(namespace)s
                and repository = %(repository)s
        )
        """
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        values: Dict[str, PrimitiveVal] = {
            "hash": id_obj.hash.hash,
            "namespace": id_obj.repo.namespace,
            "repository": id_obj.repo.repository,
        }
        query = Query.dynamic_query(statement, freeze(identifiers))

        return self._sql_client.execute(
            query, QueryValues(freeze(values))
        ) + self._sql_client.fetch_one().map(lambda x: x.unwrap()).map(
            lambda r: to_primitive(r.data[0], bool).alt(Exception).unwrap()
        )

    def init_table(self) -> Cmd[None]:
        statement = """
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            file_path VARCHAR(1024),
            hash CHAR(40),
            namespace VARCHAR(64),
            repository VARCHAR(4096),

            PRIMARY KEY (
                namespace,
                repository,
                hash,
                file_path
            )
        ) SORTKEY (namespace, repository)
        """
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        return self._sql_client.execute(
            Query.dynamic_query(statement, freeze(identifiers)), None
        )
