from ctx import (
    CTX,
)
from lib_path.analyze import (
    analyze as analyze_paths,
)
from lib_root.analyze import (
    analyze as analyze_root,
)
from model.core_model import (
    FindingEnum,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Dict,
)


def analyze(stores: Dict[FindingEnum, EphemeralStore]) -> None:
    if CTX.config.path.lib_path:
        analyze_paths(stores=stores)
    if CTX.config.path.lib_root:
        analyze_root(stores=stores)
