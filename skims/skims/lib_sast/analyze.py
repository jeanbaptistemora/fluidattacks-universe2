from ctx import (
    CTX,
)
from lib_path.analyze import (
    analyze as analyze_paths,
)
from lib_root.analyze import (
    analyze as analyze_root,
)
from lib_sast.types import (
    Paths,
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
from utils.logs import (
    log_blocking,
)


def analyze(stores: Dict[FindingEnum, EphemeralStore]) -> None:
    paths = Paths(CTX.config.path.include, CTX.config.path.exclude)

    log_blocking("info", "Files to be tested: %s", len(paths.ok_paths))

    if CTX.config.path.lib_path:
        analyze_paths(paths=paths, stores=stores)

    if CTX.config.path.lib_root:
        paths.set_lang()
        analyze_root(paths=paths, stores=stores)
