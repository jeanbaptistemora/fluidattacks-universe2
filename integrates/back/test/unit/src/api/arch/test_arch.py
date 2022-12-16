from .arch import (
    project_dag,
)

ROOT = "api"


def test_dag_creation() -> None:
    project_dag()
