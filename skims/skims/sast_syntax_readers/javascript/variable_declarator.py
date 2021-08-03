from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(node_attrs["label_field_value"])),
            ]
            if "label_field_value" in node_attrs
            else [],
        ),
        var=args.graph.nodes[node_attrs["label_field_name"]]["label_text"],
    )
