from fa_purity import (
    FrozenDict,
    FrozenList,
)
from typing import (
    Dict,
)

_DAG: Dict[str, FrozenList[str]] = {
    "target_s3": (
        "cli",
        "loader",
        "csv",
        "core",
        "in_buffer",
    ),
    "target_s3.core": (
        "_record_group",
        "_complete_record",
        "_plain_record",
        "_ro_file",
    ),
}
DAG = FrozenDict(_DAG)
