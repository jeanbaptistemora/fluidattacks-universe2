"""Fluid asserts to create Code Property Graphs."""
# Standar import
from typing import Tuple

# 3rd party imports
from networkx import DiGraph

# Local import
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.parsers import python3


def load_cpg(path: str, exclude: Tuple[str], language: str):
    """Convert the files inside the path into a properties graph."""
    graph: DiGraph = DiGraph()
    paths: Tuple[str] = get_paths(path, exclude)
    for _path in paths:
        if language == 'python':
            python3.load(graph, _path)
    return graph
