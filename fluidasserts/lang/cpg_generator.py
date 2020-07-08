"""Fluid asserts to create Code Property Graphs."""
# Standar import
from typing import Tuple

# 3rd party imports
from networkx import DiGraph

# Local import
from fluidasserts.utils.parsers import python3


def load_cpg(path: str, language: str, exclude: Tuple[str] = None):
    """Convert the files inside the path into a properties graph."""
    graph: DiGraph = DiGraph()
    if language == 'python':
        python3.create_cpg(graph, path, exclude)
    return graph
