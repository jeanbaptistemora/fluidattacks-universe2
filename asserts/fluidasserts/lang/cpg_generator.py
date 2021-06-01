"""Fluid asserts to create Code Property Graphs."""

from fluidasserts.lang import (
    GRAPHS,
    node_creator as creator,
    python3_cpg,
)
from networkx import (
    DiGraph,
)
from typing import (
    Tuple,
)


def load_cpg(path: str, language: str, exclude: Tuple[str] = None):
    """Convert the files inside the path into a properties graph."""
    graph: DiGraph = GRAPHS.get()

    creator.meta_data(graph, language=language)
    if language == "python":
        python3_cpg.create_cpg(path, exclude)
    return graph
