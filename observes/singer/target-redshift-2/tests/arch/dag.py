from fa_purity import (
    FrozenDict,
    FrozenList,
)
from typing import (
    Dict,
)

_DAG: Dict[str, FrozenList[str]] = {
    "target_redshift": (
        "cli",
        "loader",
        "data_schema",
        "errors",
        "_logger",
    ),
    "target_redshift.loader": (
        "_handlers",
        "_grouper",
        "_strategy",
        "_s3_loader",
        "_truncate",
    ),
    "target_redshift.data_schema": (
        "_data_types",
        "_utils",
    ),
    "target_redshift.data_schema._data_types": (
        "_number",
        "_string",
        "_integer",
    ),
    "target_redshift.cli": ("_upload", "_from_s3", "_core"),
}

DAG = FrozenDict(_DAG)
