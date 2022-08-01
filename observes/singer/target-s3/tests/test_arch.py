import grimp
from typing import (
    Any,
    Callable,
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


def _map_over_children(
    graph: Any, module: str, function: Callable[[str, str], None]
) -> None:
    children = frozenset(graph.find_children(module))
    for c in children:
        function(module, c)
        _map_over_children(graph, c, function)


def test_arch() -> None:
    root = "target_s3"
    graph = grimp.build_graph(root)
    _map_over_children(
        graph, root, lambda p, m: _check_private_imports(graph, p, m)
    )
