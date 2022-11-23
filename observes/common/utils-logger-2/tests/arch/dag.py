from fa_purity import (
    FrozenDict,
    FrozenList,
)
from typing import (
    Dict,
)

_DAG: Dict[str, FrozenList[str]] = {
    "utils_logger_2": ("logger", "handlers", "levels", "env"),
}
DAG = FrozenDict(_DAG)
