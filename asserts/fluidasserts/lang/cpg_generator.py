"""Fluid asserts to create Code Property Graphs."""
# Standar import
from typing import Tuple

# 3rd party imports
from networkx import DiGraph

# Local import
from fluidasserts.lang import python3_cpg
from fluidasserts.lang import node_creator as creator
from fluidasserts.lang import GRAPHS


def load_cpg(path: str, language: str, exclude: Tuple[str] = None):
    """Convert the files inside the path into a properties graph."""
    graph: DiGraph = GRAPHS.get()

    creator.meta_data(graph, language=language)
    if language == 'python':
        python3_cpg.create_cpg(path, exclude)
    return graph
