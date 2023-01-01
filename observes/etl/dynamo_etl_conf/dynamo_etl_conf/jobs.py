from dataclasses import (
    dataclass,
)
from dynamo_etl_conf import (
    drivers,
)
from dynamo_etl_conf._run import (
    external_run,
)
from dynamo_etl_conf.core import (
    TargetTables,
)
from enum import (
    Enum,
)
from fa_purity.cmd import (
    Cmd,
)
import os


class Jobs(Enum):
    CORE = "CORE"
    DETERMINE_SCHEMA = "DETERMINE_SCHEMA"
    CORE_PREPARE = "CORE_PREPARE"


@dataclass(frozen=True)
class Executor:
    _schema_prefix: str
    _etl_parallel: str
    _etl_prepare: str

    def core(self) -> Cmd[None]:
        args = [
            self._etl_parallel,
            "30",  # total_segments: MUST coincide with batch parallel conf
            "auto",
        ]
        # [!] REMEMBER: adjust centralizer range according to total_segments
        return external_run(tuple(args))

    def prepare_core(self) -> Cmd[None]:
        args = [
            self._etl_prepare,
            f"dynamodb_integrates_vms_merged_parts_loading",
            "s3://observes.cache/dynamoEtl/vms_schema",
        ]
        return external_run(tuple(args))

    def determine_schema(self) -> Cmd[None]:
        return drivers.determine_schema(
            frozenset([TargetTables.CORE.value]),
            100,
            "s3://observes.cache/dynamoEtl/vms_schema",
        )


def default_executor() -> Executor:
    return Executor(
        "dynamodb_",
        os.environ["DYNAMO_PARALLEL"],
        os.environ["DYNAMO_PREPARE"],
    )


def run_job(exe: Executor, job: Jobs) -> Cmd[None]:
    if job is Jobs.CORE:
        return exe.core()
    if job is Jobs.CORE_PREPARE:
        return exe.prepare_core()
    if job is Jobs.DETERMINE_SCHEMA:
        return exe.determine_schema()
