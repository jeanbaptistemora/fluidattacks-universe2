from enum import (
    Enum,
)
from fa_purity.frozen import (
    FrozenDict,
)


class TargetTables(Enum):
    CORE = "integrates_vms"


_tt = TargetTables
SEGMENTATION: FrozenDict[TargetTables, int] = FrozenDict(
    {
        _tt.CORE: 100,
    }
)
