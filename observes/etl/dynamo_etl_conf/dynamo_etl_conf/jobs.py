from dataclasses import (
    dataclass,
)
from dynamo_etl_conf._run import (
    external_run,
)
from dynamo_etl_conf.core import (
    SEGMENTATION,
    TargetTables,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.frozen import (
    FrozenList,
)
import os


@dataclass(frozen=True)
class Jobs:
    _schema_prefix: str = "dynamodb_"
    _etl_bin: str = os.environ["DYNAMO_ETL_BIN"]
    _etl_big_bin: str = os.environ["DYNAMO_ETL_BIG_BIN"]

    def run(
        self, schema: str, tables: FrozenList[str], segments: int, big: bool
    ) -> Cmd[None]:
        _bin = self._etl_big_bin if big else self._etl_bin
        return external_run(
            tuple([_bin, schema, " ".join(tables), str(segments)])
        )

    def default_run(self, table: TargetTables, big: bool = False) -> Cmd[None]:
        return self.run(
            f"{self._schema_prefix}{table.value}",
            (table.value,),
            SEGMENTATION[table],
            big,
        )

    def standard_group(self) -> Cmd[None]:
        cmds = tuple(
            self.default_run(table)
            for table in TargetTables
            if table not in (TargetTables.CORE, TargetTables.FORCES)
        )
        return serial_merge(cmds).map(lambda _: None)

    def forces(self) -> Cmd[None]:
        return self.default_run(TargetTables.FORCES)

    def core(self) -> Cmd[None]:
        return self.default_run(TargetTables.CORE, True)
