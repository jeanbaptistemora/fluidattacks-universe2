from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "catch_formal_parameter",
    )
    parameter = match["catch_formal_parameter"]
    match = g.match_ast(
        args.graph,
        str(parameter),
        "catch_type",
        "identifier",
    )
    catch_types = (
        n_id
        for n_id in g.adj(args.graph, str(match["catch_type"]))
        if args.graph.nodes[n_id]["label_type"] != "|"
    )
    for type_id in catch_types:
        yield graph_model.SyntaxStepCatchClause(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=type_id,
            ),
            var=args.graph.nodes[match["identifier"]]["label_text"],
            catch_type=args.graph.nodes[type_id]["label_text"],
        )
