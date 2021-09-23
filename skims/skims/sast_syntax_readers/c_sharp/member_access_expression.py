from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils.graph import (
    match_ast_group,
)
from utils.graph.transformation import (
    get_base_identifier_id,
    node_to_str,
)
from utils.string import (
    split_on_first_dot,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match_access = match_ast_group(
        args.graph,
        args.n_id,
        "identifier",
        "__0__",
        "this_expression",
        ".",
    )
    expression_str = node_to_str(args.graph, args.n_id)
    _, member = split_on_first_dot(expression_str)

    if expression := match_access["__0__"]:
        dependence = args.generic(args.fork_n_id(expression))
    else:
        mem_acces = "member_access_expression"
        base_ident = get_base_identifier_id(args.graph, args.n_id, mem_acces)

        if not base_ident:
            raise MissingCaseHandling(args)

        dependence = args.generic(args.fork_n_id(base_ident))

    yield graph_model.SyntaxStepMemberAccessExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [dependence],
        ),
        member=member,
        expression=expression_str,
    )
