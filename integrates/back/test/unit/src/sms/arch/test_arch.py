from .arch import (
    project_dag,
)
from arch_lint import (
    FullPathModule,
)
from arch_lint.dag.check import (
    check_dag_map,
    dag_map_completeness,
)
from arch_lint.graph import (
    ImportGraph,
)

root = FullPathModule.assert_module("sms")


def test_dag_creation() -> None:
    project_dag()


def test_dag_completeness() -> None:
    graph = ImportGraph.from_modules(root, True)
    dag_map_completeness(project_dag(), graph, root)


def test_dag() -> None:
    graph = ImportGraph.from_modules(root, True)
    check_dag_map(project_dag(), graph)
