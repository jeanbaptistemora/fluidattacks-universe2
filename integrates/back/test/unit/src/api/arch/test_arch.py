from .arch import (
    project_dag,
)
from arch_lint.dag.check import (
    check_dag_map,
)
from arch_lint.graph import (
    ImportGraph,
)

ROOT = "api"


def test_dag_creation() -> None:
    project_dag()


def test_dag() -> None:
    graph = ImportGraph.build_graph(ROOT, False)
    check_dag_map(project_dag(), graph)
