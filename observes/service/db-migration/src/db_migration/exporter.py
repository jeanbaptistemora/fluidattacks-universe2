from dataclasses import (
    dataclass,
)
from db_migration._patch import (
    Patch,
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
import logging
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.table.client import (
    ManifestId,
    TableClient,
)
from typing import (
    Callable,
    Tuple,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Exporter:
    table_client_r: TableClient
    table_client_w: TableClient
    schema_client_r: SchemaClient
    schema_client_w: SchemaClient
    schema_filter: Patch[Callable[[SchemaId], bool]]
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
                        for s in filter(self.schema_filter.unwrap, schemas)
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

    def export_to_s3(self) -> Cmd[PureIter[Tuple[TableId, ManifestId]]]:
        return (
            self.target_tables()
            .map(
                lambda p: p.map(
                    lambda t: self.export_table(t).map(lambda m: (t, m))
                ).to_list()
            )
            .bind(lambda x: serial_merge(x))
            .map(lambda l: from_flist(l))
        )

    def import_from_s3(
        self, manifests: PureIter[Tuple[TableId, ManifestId]]
    ) -> Cmd[None]:
        return manifests.map(
            lambda i: self.import_table(i[0], i[1])
        ).transform(consume)

    def migrate(self) -> Cmd[None]:
        return self.export_to_s3().bind(self.import_from_s3)
