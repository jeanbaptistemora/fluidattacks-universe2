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
from typing import (
    Literal,
    Union,
)


@dataclass(frozen=True)
class Jobs:
    _schema_prefix: str = "dynamodb_"
    _ELT_bin: str = os.environ["DYNAMO_ETL_BIN"]

    def run(
        self, schema: str, tables: FrozenList[str], segments: int
    ) -> Cmd[None]:
        return external_run(
            tuple([self._ELT_bin, schema, " ".join(tables), str(segments)])
        )

    def standard_group(self) -> Cmd[None]:
        cmds = tuple(
            self.run(
                f"{self._schema_prefix}{table.value}",
                (table.value,),
                SEGMENTATION[table],
            )
            for table in TargetTables
            if table not in (TargetTables.CORE, TargetTables.FORCES)
        )
        return serial_merge(cmds).map(lambda _: None)

    def non_grouped(
        self,
        target: Union[
            Literal[TargetTables.CORE], Literal[TargetTables.FORCES]
        ],
    ) -> Cmd[None]:
        target_str: str = target.value
        return self.run(
            f"{self._schema_prefix}{target_str}",
            (target_str,),
            SEGMENTATION[target],
        )
