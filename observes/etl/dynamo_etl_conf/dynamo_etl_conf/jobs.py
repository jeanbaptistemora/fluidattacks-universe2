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
from enum import (
    Enum,
)
from fa_purity import (
    Maybe,
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


class Jobs(Enum):
    FORCES = "FORCES"
    CORE = "CORE"
    CORE_NO_CACHE = "CORE_NO_CACHE"
    CORE_PREPARE = "CORE_PREPARE"
    GROUP = "GROUP"


@dataclass(frozen=True)
class Executor:
    _schema_prefix: str
    _etl_bin: str
    _etl_big_bin: str
    _etl_parrallel: str
    _etl_prepare: str

    def _run(
        self,
        schema: str,
        tables: FrozenList[str],
        segments: int,
        big: bool,
        cache: Maybe[str],
        use_cache: bool,
    ) -> Cmd[None]:
        _bin = self._etl_big_bin if big else self._etl_bin
        return external_run(
            tuple([_bin, schema, " ".join(tables), str(segments)])
            + ("yes" if use_cache else "no", cache.value_or("none"))
        )

    def _default_run(
        self,
        table: TargetTables,
        big: bool,
        cache: Maybe[str],
        use_cache: bool,
    ) -> Cmd[None]:
        return self._run(
            f"{self._schema_prefix}{table.value}",
            (table.value,),
            SEGMENTATION[table],
            big,
            cache,
            use_cache,
        )

    def standard_group(self) -> Cmd[None]:
        cmds = tuple(
            self._default_run(table, False, Maybe.empty(), False)
            for table in TargetTables
            if table not in (TargetTables.CORE, TargetTables.FORCES)
        )
        return serial_merge(cmds).map(lambda _: None)

    def forces(self) -> Cmd[None]:
        return self._default_run(
            TargetTables.FORCES, False, Maybe.empty(), False
        )

    def core(self) -> Cmd[None]:
        return self._default_run(
            TargetTables.CORE,
            True,
            Maybe.from_value("s3://observes.cache/dynamoEtl/vms_schema"),
            True,
        )

    def prepare_core(self) -> Cmd[None]:
        table = TargetTables.CORE
        args = [
            self._etl_prepare,
            f"{self._schema_prefix}{table.value}_loading",
            "s3://observes.cache/dynamoEtl/vms_schema",
        ]
        return external_run(tuple(args))

    def core_no_cache(self) -> Cmd[None]:
        table = TargetTables.CORE
        args = [
            self._etl_parrallel,
            f"{self._schema_prefix}{table.value}_loading",
            table.value,
            "50",  # total_segments: MUST coincide with batch parallel conf
            "s3://observes.cache/dynamoEtl/vms_schema",
        ]
        return external_run(tuple(args))


def default_executor() -> Executor:
    return Executor(
        "dynamodb_",
        os.environ["DYNAMO_ETL_BIN"],
        os.environ["DYNAMO_ETL_BIG_BIN"],
        os.environ["DYNAMO_PARALLEL"],
        os.environ["DYNAMO_PREPARE"],
    )


def run_job(exe: Executor, job: Jobs) -> Cmd[None]:
    if job is Jobs.FORCES:
        return exe.forces()
    if job is Jobs.CORE:
        return exe.core()
    if job is Jobs.CORE_NO_CACHE:
        return exe.core_no_cache()
    if job is Jobs.CORE_PREPARE:
        return exe.prepare_core()
    if job is Jobs.GROUP:
        return exe.standard_group()
