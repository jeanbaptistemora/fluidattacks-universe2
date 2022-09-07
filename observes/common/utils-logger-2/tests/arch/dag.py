# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
