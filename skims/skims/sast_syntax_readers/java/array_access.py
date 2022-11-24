from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    yield graph_model.SyntaxStepArrayAccess(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(node_attrs["label_field_array"])),
                args.generic(args.fork_n_id(node_attrs["label_field_index"])),
            ],
        ),
    )
