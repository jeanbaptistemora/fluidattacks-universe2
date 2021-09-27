from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph import (
    match_ast_group,
)
from utils.graph.transformation import (
    get_text_childs,
    n_ids_to_str,
)
from utils.string import (
    split_on_first_dot,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match_access = match_ast_group(
        args.graph,
        args.n_id,
        "identifier",
        "this_expression",
        ".",
        "__0__",
    )

    n_ids = get_text_childs(args.graph, args.n_id)
    expression_str = n_ids_to_str(args.graph, n_ids)
    _, member = split_on_first_dot(expression_str)

    if expression := match_access["__0__"]:
        dependence = args.generic(args.fork_n_id(expression))
    else:
        base_ident, *_ = n_ids
        dependence = args.generic(args.fork_n_id(base_ident))

    yield graph_model.SyntaxStepMemberAccessExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [dependence],
        ),
        member=member,
        expression=expression_str,
    )
