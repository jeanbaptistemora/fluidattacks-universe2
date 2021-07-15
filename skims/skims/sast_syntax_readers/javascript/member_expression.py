from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph.transformation import (
    build_js_member_expression_ids,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    ids = build_js_member_expression_ids(args.graph, args.n_id)
    yield from args.generic(args.fork_n_id(ids[-1]))
