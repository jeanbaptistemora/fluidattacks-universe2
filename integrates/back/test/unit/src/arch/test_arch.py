from .arch import (
    project_dag,
)
from arch_lint.dag.check import (
    check_dag,
)
from arch_lint.graph import (
    ImportGraph,
)
import pytest

ROOT = "integrates"


def test_dag_creation() -> None:
    project_dag()


@pytest.mark.xfail
def test_dag() -> None:
    graph = ImportGraph.build_graph(ROOT, True)
    check_dag(project_dag(), graph, graph.root)
