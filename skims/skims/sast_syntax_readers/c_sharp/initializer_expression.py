from model import (
    graph_model,
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


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    assig_exp = "assignment_expression"

    for assign_exp_id in g.match_ast_group_d(args.graph, args.n_id, assig_exp):
        attr = args.graph.nodes[assign_exp_id]
        var_id = attr["label_field_left"]
        value_id = attr["label_field_right"]

        if args.graph.nodes[var_id]["label_type"] != "identifier":
            raise MissingCaseHandling(args)

        yield graph_model.SyntaxStepNamedArgument(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                dependencies=[
                    args.generic(args.fork_n_id(value_id)),
                ],
            ),
            var=node_to_str(args.graph, var_id),
        )
