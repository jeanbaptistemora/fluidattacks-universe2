from .arch import (
    forbidden_allowlist,
    project_dag,
)
from arch_lint.dag.check import (
    check_dag_map,
    dag_map_completeness,
)
from arch_lint.forbidden import (
    check_forbidden,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from arch_lint.private import (
    check_private,
)

root = FullPathModule.assert_module("tap_json")
local_graph = ImportGraph.from_modules(root, False)
ext_graph = ImportGraph.from_modules(root, True)


def test_dag_creation() -> None:
    project_dag()


def test_dag() -> None:
    check_dag_map(project_dag(), local_graph)


def test_dag_completeness() -> None:
    dag_map_completeness(project_dag(), local_graph, root)


def test_forbidden_creation() -> None:
    forbidden_allowlist()


def test_forbidden() -> None:
    allowlist_map = forbidden_allowlist()
    check_forbidden(allowlist_map, ext_graph)


def test_private() -> None:
    check_private(ext_graph, root)
