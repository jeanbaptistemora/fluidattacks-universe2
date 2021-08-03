from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    yield from args.generic(
        args.fork_n_id(args.graph.nodes[args.n_id]["label_field_parameters"])
    )
