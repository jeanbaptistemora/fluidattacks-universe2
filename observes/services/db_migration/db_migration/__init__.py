from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.pure_iter.core import (
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    chain,
)
import os
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.schema.core import (
    SchemaId,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    IsolationLvl,
)
from redshift_client.sql_client.core import (
    new_client,
)
from redshift_client.table.client import (
    ManifestId,
    TableClient,
)
from redshift_client.table.core import (
    TableId,
)
from typing import (
    Callable,
    Tuple,
)
from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "0.1.0"
set_bugsnag(BugsnagConf("service", __version__, __file__, True))
LOG = set_main_log(__name__)


def creds_from_env() -> Credentials:
    return Credentials(
        os.environ["DB_USER"],
        os.environ["DB_PASSWORD"],
    )


def db_from_env() -> DatabaseId:
    return DatabaseId(
        os.environ["DB_NAME"],
        os.environ["DB_HOST"],
        int(os.environ["DB_PORT"]),
    )


@dataclass(frozen=True)
class Exporter:
    table_client_R: TableClient
    table_client_W: TableClient
    schema_client_R: SchemaClient
    bucket: str
    role: str

    def export_table(self, table: TableId) -> Cmd[ManifestId]:
        prefix = f"{self.bucket}/{table.schema.name}/{table.name}_"
        return self.table_client_R.unload(table, prefix, self.role)

    def target_tables(self) -> Cmd[PureIter[TableId]]:
        filter_fx: Callable[
            [SchemaId], bool
        ] = lambda s: not s.name.startswith("pg_")
        return (
            self.schema_client_R.all_schemas()
            .bind(
                lambda schemas: serial_merge(
                    tuple(
                        self.schema_client_R.table_ids(s).map(
                            lambda x: from_flist(tuple(x))
                        )
                        for s in filter(filter_fx, schemas)
                    )
                )
            )
            .map(lambda x: from_flist(x))
            .map(lambda x: chain(x))
        )

    def export_to_s3(self) -> Cmd[None]:
        tables = self.target_tables()
        manifests = tables.map(
            lambda p: p.map(
                lambda t: self.export_table(t).map(lambda m: (t, m))
            ).to_list()
        ).bind(lambda x: serial_merge(x))
        unload = (
            manifests.map(
                lambda l: tuple(
                    self.table_client_W.load(i[0], i[1], self.role) for i in l
                )
            )
            .bind(lambda x: serial_merge(x))
            .map(lambda _: None)
        )
        return unload


def main(
    old: Tuple[DatabaseId, Credentials], new: Tuple[DatabaseId, Credentials]
) -> Cmd[None]:
    connection_R = connect(old[0], old[1], True, IsolationLvl.AUTOCOMMIT)
    connection_W = connect(new[0], new[1], False, IsolationLvl.AUTOCOMMIT)
    client_R = connection_R.bind(lambda c: new_client(c, LOG))
    client_W = connection_W.bind(lambda c: new_client(c, LOG))
    exporter = client_R.bind(
        lambda r: client_W.map(
            lambda w: Exporter(
                TableClient(r),
                TableClient(w),
                SchemaClient(r),
                "s3://the_bucktet",
                "arn:aws:iam::<aws-account-id>:role/<role-name>",
            )
        )
    )
    return exporter.bind(lambda e: e.export_to_s3())
