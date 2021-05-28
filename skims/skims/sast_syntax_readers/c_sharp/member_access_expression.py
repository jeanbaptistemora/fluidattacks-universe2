# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.string import split_on_first_dot
from utils.graph import match_ast_group
from utils.graph.transformation import (
    build_member_access_expression_isd,
    build_member_access_expression_key,
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
    _, access_key = split_on_first_dot(
        build_member_access_expression_key(args.graph, args.n_id)
    )
    if expression := match_access["__0__"]:
        dependence = args.generic(args.fork_n_id(expression))
    else:
        members = build_member_access_expression_isd(args.graph, args.n_id)
        dependence = args.generic(args.fork_n_id(members[0]))
    yield graph_model.SyntaxStepMemberAccessExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [dependence],
        ),
        member=access_key,
    )
