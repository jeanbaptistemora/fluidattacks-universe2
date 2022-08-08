from fa_purity import (
    FrozenDict,
    FrozenList,
)
from typing import (
    Dict,
)

_DAG: Dict[str, FrozenList[str]] = {
    "target_s3": (
        "_cli",
        "loader",
        "upload",
        "csv",
        "_splitter",
        "core",
        "in_buffer",
        "_utils",
    ),
    "target_s3.core": (
        "_record_group",
        "_complete_record",
        "_plain_record",
        "_ro_file",
    ),
}
DAG = FrozenDict(_DAG)
