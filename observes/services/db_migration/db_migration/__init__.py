from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
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
    consume,
)
import os
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.schema.client import (
    SchemaClient,
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


class EnvVarPrefix(Enum):
    SOURCE = "SOURCE"
    TARGET = "TARGET"


def from_env(prefix: EnvVarPrefix) -> Tuple[DatabaseId, Credentials]:
    creds = Credentials(
        os.environ[f"{prefix.value}_DB_USER"],
        os.environ[f"{prefix.value}_DB_PASSWORD"],
    )
    db = DatabaseId(
        os.environ[f"{prefix.value}_DB_NAME"],
        os.environ[f"{prefix.value}_DB_HOST"],
        int(os.environ[f"{prefix.value}_DB_PORT"]),
    )
    return (db, creds)


EPHEMERAL_SCHEMAS = frozenset(
    [
        "announcekit",
        "bugsnag",
        "checkly",
        "delighted",
        "formstack",
        "mailchimp",
        "mixpanel_integrates",
        "timedoctor",
        "zoho_crm",
    ]
)


@dataclass(frozen=True)
class Exporter:
    table_client_R: TableClient
    table_client_W: TableClient
    schema_client_R: SchemaClient
    bucket: str
    role: str

    def export_table(self, table: TableId) -> Cmd[ManifestId]:
        prefix = f"{self.bucket}/{table.schema.name}/{table.name}/"
        return self.table_client_R.unload(table, prefix, self.role)

    def target_tables(self) -> Cmd[PureIter[TableId]]:
        filter_fx: Callable[[SchemaId], bool] = lambda s: all(
            [
                not s.name.startswith("pg_"),
                not s.name.startswith("dynamodb_"),
                not s.name.endswith("backup"),
                not s.name == "information_schema",
                not s.name in EPHEMERAL_SCHEMAS,
            ]
        )
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
        manifests = (
            self.target_tables()
            .map(
                lambda p: p.map(
                    lambda t: self.export_table(t).map(lambda m: (t, m))
                ).to_list()
            )
            .bind(lambda x: serial_merge(x))
        )
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
) -> Cmd[Exporter]:
    connection_R = connect(old[0], old[1], True, IsolationLvl.AUTOCOMMIT)
    connection_W = connect(new[0], new[1], False, IsolationLvl.AUTOCOMMIT)
    client_R = connection_R.bind(lambda c: new_client(c, LOG))
    client_W = connection_W.bind(lambda c: new_client(c, LOG))
    return client_R.bind(
        lambda r: client_W.map(
            lambda w: Exporter(
                TableClient(r),
                TableClient(w),
                SchemaClient(r),
                "s3://observes.migration",
                "arn:aws:iam::205810638802:role/redshift-role",
            )
        )
    )
