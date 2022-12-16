from .arch import (
    project_dag,
)
from arch_lint.dag.check import (
    check_dag,
    dag_completeness_from_dir,
)
from arch_lint.graph import (
    ImportGraph,
)
from pathlib import (
    Path,
)
import pytest


def test_dag_creation() -> None:
    project_dag()


@pytest.mark.xfail
def test_dag() -> None:
    graph = ImportGraph.from_modules(project_dag().all_modules, False)
    check_dag(project_dag(), graph)


def test_dag_completeness_from_dir() -> None:
    dag_completeness_from_dir(project_dag(), Path("./back/src/"), True, None)
