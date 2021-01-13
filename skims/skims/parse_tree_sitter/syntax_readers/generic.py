# Standard library
from typing import (
    Callable,
    Set,
    Tuple,
)

# Local libraries
from model import (
    graph_model,
)
from utils import (
    graph as g,
)
from utils.function import (
    get_id,
)
from utils.logs import (
    log_blocking,
)


LabelTypes = Set[str]
SyntaxReader = Callable[
    [graph_model.Graph, graph_model.NId, graph_model.SyntaxSteps],
    None,
]
SyntaxReaders = Tuple[SyntaxReader, ...]


class UnableToRead(Exception):

    def __init__(self, reader: SyntaxReader, n_id: graph_model.NId) -> None:
        log_blocking('debug', 'Unable to read: %s, %s', get_id(reader), n_id)
        super().__init__()


def method_declaration(
    graph: graph_model.Graph,
    n_id: graph_model.NId,
    syntax_steps: graph_model.SyntaxSteps,
) -> None:
    for params_id in g.get_ast_childs(graph, n_id, 'formal_parameters'):
        for param_id in g.get_ast_childs(graph, params_id, 'formal_parameter'):
            method_declaration_formal_parameter(graph, param_id, syntax_steps)


def method_declaration_formal_parameter(
    graph: graph_model.Graph,
    n_id: graph_model.NId,
    syntax_steps: graph_model.SyntaxSteps,
) -> None:
    match = g.match_ast(graph, n_id, 'type_identifier', 'identifier')

    if (
        len(match) == 2
        and (var_type_id := match['type_identifier'])
        and (var_id := match['identifier'])
    ):
        syntax_steps.append(graph_model.SyntaxStepDeclaration(
            dependencies=[],
            meta=graph_model.SyntaxStepMeta.default(),
            var=graph.nodes[var_id]['label_text'],
            var_type=graph.nodes[var_type_id]['label_text'],
        ))
    else:
        raise UnableToRead(
            reader=method_declaration_formal_parameter,
            n_id=n_id,
        )


def attemp_with_readers(
    graph: graph_model.Graph,
    n_id: graph_model.NId,
    syntax_readers: SyntaxReaders,
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    for syntax_reader in syntax_readers:
        try:
            syntax_reader(graph, n_id, syntax_steps)
        except UnableToRead:
            # This syntax reader is not able to understand the node
            continue
        else:
            # This syntax reader was able to understand the node
            # Let's read the next node
            break

    return syntax_steps


DISPATCHERS: Tuple[Tuple[LabelTypes, SyntaxReaders], ...] = (
    ({'method_declaration'},
     (method_declaration,)),
)


def read_from_graph(
    graph: graph_model.Graph,
) -> graph_model.GraphSyntax:
    graph_syntax: graph_model.GraphSyntax = {}

    for n_id, n_attrs in graph.nodes.items():
        syntax_steps: graph_model.SyntaxSteps = []

        for label_types, syntax_readers in DISPATCHERS:
            if n_attrs['label_type'] in label_types:
                syntax_steps = attemp_with_readers(
                    graph=graph,
                    n_id=n_id,
                    syntax_readers=syntax_readers,
                )

        graph_syntax[n_id] = syntax_steps

    return graph_syntax
