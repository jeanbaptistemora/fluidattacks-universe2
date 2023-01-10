from ._bins import (
    BinPaths,
)
from dynamo_etl_conf._run import (
    external_run,
)
from fa_purity.cmd import (
    Cmd,
)
from typing import (
    FrozenSet,
)


def determine_schema(
    tables: FrozenSet[str], segments: int, cache_bucket: str
) -> Cmd[None]:
    args = (
        BinPaths.DETERMINE_SCHEMAS.value,
        " ".join(tables),
        str(segments),
        cache_bucket,
    )
    return external_run(args)


def prepare_loading(loading_schema: str, cache_bucket: str) -> Cmd[None]:
    args = (
        BinPaths.PREPARE_LOADING.value,
        loading_schema,
        cache_bucket,
    )
    return external_run(args)
