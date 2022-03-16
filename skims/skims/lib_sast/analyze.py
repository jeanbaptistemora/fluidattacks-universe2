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
from utils.fs import (
    resolve_paths,
)


def analyze(stores: Dict[FindingEnum, EphemeralStore]) -> None:
    paths = resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    if CTX.config.path.lib_path:
        analyze_paths(paths=paths, stores=stores)

    if CTX.config.path.lib_root:
        analyze_root(paths=paths, stores=stores)
