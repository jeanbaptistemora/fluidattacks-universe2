from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepDefaultParameter,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node = args.graph.nodes[args.n_id]
    childs = g.adj_ast(args.graph, args.n_id)

    type_id = node.get("label_field_type")
    identifier_id = node.get("label_field_name")

    var = args.graph.nodes[identifier_id]["label_text"]
    var_type = None if type_id is None else node_to_str(args.graph, type_id)

    if len(childs) <= 2:
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=var,
            var_type=var_type,
        )
    else:
        if eq_c := g.match_ast_d(args.graph, args.n_id, "equals_value_clause"):
            match = g.match_ast(args.graph, eq_c, "=")

            if len(match) != 2:
                raise MissingCaseHandling(args)

            yield SyntaxStepDefaultParameter(
                meta=SyntaxStepMeta.default(
                    args.n_id,
                    dependencies=[
                        args.generic(args.fork_n_id(match["__0__"])),
                    ],
                ),
                var=var,
                var_type=var_type,
            )
        else:
            raise MissingCaseHandling(args)
