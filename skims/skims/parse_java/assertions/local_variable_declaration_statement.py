# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
)
from utils import (
    graph as g,
)


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.Context
) -> None:
    # localVariableDeclarationStatement = localVariableDeclaration ';'
    match = g.match_ast(graph, n_id, 'LocalVariableDeclaration')
    if c_id := match['LocalVariableDeclaration']:
        _local_variable_declaration(graph, c_id, ctx=ctx)


def _local_variable_declaration(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.Context
) -> None:
    # variableModifier* unannType variableDeclaratorList
    # Mostly due to reducers this end up being:
    # - CustomUnannClassOrInterfaceType VariableDeclarator
    # - IdentifierRule VariableDeclarator
    common.warn_not_impl(
        _local_variable_declaration, graph=graph, n_id=n_id, ctx=ctx,
    )
