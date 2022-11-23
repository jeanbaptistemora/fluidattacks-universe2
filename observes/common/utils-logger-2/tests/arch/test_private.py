from ._utils import (
    map_over_children,
)
import grimp
from typing import (
    Any,
    FrozenSet,
)


def _check_private_imports(graph: Any, parent: str, module: str) -> None:
    importers: FrozenSet[str] = frozenset(
        graph.find_modules_that_directly_import(module)
    )
    is_private = module.removeprefix(parent + ".").startswith("_")

    def _valid_importer(importer: str) -> bool:
        return importer.startswith(parent)

    if is_private:
        for i in importers:
            if not _valid_importer(i):
                raise Exception(f"Illegal import {i} -> {module}")
    return None


def test_private() -> None:
    root = "utils_logger_2"
    graph = grimp.build_graph(root)
    map_over_children(
        graph, root, lambda p, m: _check_private_imports(graph, p, m)
    )
