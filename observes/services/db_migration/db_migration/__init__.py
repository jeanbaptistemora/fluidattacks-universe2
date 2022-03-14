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
    ]
)

TARGETS = frozenset(
    [
        "zoho_crm",
        "code",
        "gitlab-ci",
    ]
)


def _schema_filter(schema: SchemaId) -> bool:
    return all(
        [
            not schema.name.startswith("pg_"),
            not schema.name.startswith("dynamodb_"),
            not schema.name.endswith("backup"),
            not schema.name == "information_schema",
            not schema.name in EPHEMERAL_SCHEMAS,
            schema.name in TARGETS,
        ]
    )


@dataclass(frozen=True)
class Exporter:
    table_client_r: TableClient
    table_client_w: TableClient
    schema_client_r: SchemaClient
    schema_client_w: SchemaClient
    bucket: str
    role: str

    def export_table(self, table: TableId) -> Cmd[ManifestId]:
        msg = Cmd.from_cmd(lambda: LOG.info("Exporting %s...", table))

        def msg_done(m: ManifestId) -> Cmd[ManifestId]:
            _msg = Cmd.from_cmd(
                lambda: LOG.info("[EXPORTED] %s -> %s", table, m.uri)
            )
            return _msg.map(lambda _: m)

        create_schema = self.schema_client_w.create(table.schema, True)
        create_table = self.table_client_r.get(table).bind(
            lambda t: self.table_client_w.new(table, t)
        )
        prefix = f"{self.bucket}/{table.schema.name}/{table.name}/"
        return (
            msg
            + create_schema
            + create_table
            + self.table_client_r.unload(table, prefix, self.role).bind(
                msg_done
            )
        )

    def target_tables(self) -> Cmd[PureIter[TableId]]:
        return (
            self.schema_client_r.all_schemas()
            .bind(
                lambda schemas: serial_merge(
                    tuple(
                        self.schema_client_r.table_ids(s).map(
                            lambda x: from_flist(tuple(x))
                        )
                        for s in filter(_schema_filter, schemas)
                    )
                )
            )
            .map(lambda x: from_flist(x))
            .map(lambda x: chain(x))
        )

    def import_table(self, table: TableId, manifest: ManifestId) -> Cmd[None]:
        msg = Cmd.from_cmd(
            lambda: LOG.info("Importing %s from %s...", table, manifest.uri)
        )
        msg_done = Cmd.from_cmd(lambda: LOG.info("[IMPORTED] %s", table))
        return (
            msg
            + self.table_client_w.load(table, manifest, self.role)
            + msg_done
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
        unload = manifests.bind(
            lambda l: from_flist(l)
            .map(lambda i: self.import_table(i[0], i[1]))
            .transform(consume)
        )
        return unload


def main(
    old: Tuple[DatabaseId, Credentials], new: Tuple[DatabaseId, Credentials]
) -> Cmd[Exporter]:
    connection_r = connect(old[0], old[1], True, IsolationLvl.AUTOCOMMIT)
    connection_w = connect(new[0], new[1], False, IsolationLvl.AUTOCOMMIT)
    client_r = connection_r.bind(lambda c: new_client(c, LOG))
    client_w = connection_w.bind(lambda c: new_client(c, LOG))
    return client_r.bind(
        lambda r: client_w.map(
            lambda w: Exporter(
                TableClient(r),
                TableClient(w),
                SchemaClient(r),
                SchemaClient(w),
                "s3://observes.migration",
                "arn:aws:iam::205810638802:role/redshift-role",
            )
        )
    )
