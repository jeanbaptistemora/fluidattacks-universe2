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
from utils.graph.transformation import (
    build_js_member_expression,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    assignments = tuple(_expression(args, args.n_id))
    last_assignment = assignments[-1]
    for var_identifier in assignments[:-1]:
        yield graph_model.SyntaxStepAssignment(
            meta=last_assignment.meta,  # type: ignore
            var=var_identifier,
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
        "**=",
        "<<=",
        ">>=",
        ">>>=",
        "&=",
        "^=",
        "|=",
        "&&=",
        "||=",
        "??=",
    }
    match = g.match_ast(
        args.graph,
        expression_id,
        "__0__",
        "__1__",
        "__2__",
    )
    left_id = match["__0__"]
    operator_id = match["__1__"]
    src_id = match["__2__"]

    if args.graph.nodes[operator_id]["label_text"] not in assignment_operators:
        raise MissingCaseHandling(args)

    left_type = args.graph.nodes[left_id]["label_type"]
    if left_type == "identifier":
        identifier_name = args.graph.nodes[left_id]["label_text"]
    elif left_type == "member_expression":
        identifier_name = build_js_member_expression(args.graph, left_id)
    else:
        raise MissingCaseHandling(args)

    if args.graph.nodes[src_id]["label_type"] == "assignment_expression":
        yield identifier_name
        yield from _expression(args, src_id)
    else:
        yield graph_model.SyntaxStepAssignment(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(src_id)),
                ],
            ),
            var=identifier_name,
        )
