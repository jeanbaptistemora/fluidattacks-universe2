from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
    Union,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    assignments = tuple(_expression(args, args.n_id))
    last_assignment = assignments[-1]
    for var_identifier_id in assignments[:-1]:
        yield graph_model.SyntaxStepAssignment(
            meta=last_assignment.meta,  # type: ignore
            var=args.graph.nodes[var_identifier_id]["label_text"],
        )
    yield last_assignment


def _expression(
    args: SyntaxReaderArgs, expression_id: str
) -> Iterator[Union[str, graph_model.SyntaxStepAssignment]]:
    assignment_operators = {
        "=",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "&=",
        "^=",
        "|=",
        "<<=",
        ">>=",
        ">>>=",
    }
    match = g.match_ast(
        args.graph,
        expression_id,
        "__0__",
        "__1__",
        "__2__",
    )
    # pylint: disable=used-before-assignment
    if (
        (var_identifier_id := match["__0__"])
        and (op_id := match["__1__"])
        and (args.graph.nodes[op_id]["label_text"] in assignment_operators)
        and (src_id := match["__2__"])
    ):
        if args.graph.nodes[src_id]["label_type"] == "assignment_expression":
            yield var_identifier_id
            yield from _expression(args, src_id)
        else:
            identifier_type = args.graph.nodes[var_identifier_id]["label_type"]
            if identifier_type == "identifier":
                var_identifier_str = args.graph.nodes[var_identifier_id][
                    "label_text"
                ]
            elif identifier_type == "member_access_expression":
                var_identifier_str = g.transformation.node_to_str(
                    args.graph, var_identifier_id
                )
            else:
                raise MissingCaseHandling(args)

            yield graph_model.SyntaxStepAssignment(
                meta=graph_model.SyntaxStepMeta.default(
                    args.n_id,
                    [
                        args.generic(args.fork_n_id(src_id)),
                    ],
                ),
                var=var_identifier_str,
            )
    else:
        raise MissingCaseHandling(args)
