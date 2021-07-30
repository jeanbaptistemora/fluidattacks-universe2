from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    left_id = args.graph.nodes[args.n_id]["label_field_left"]
    left_data = args.graph.nodes[left_id]
    if left_data["label_type"] != "identifier":
        raise MissingCaseHandling(args)

    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(
                    args.fork_n_id(
                        args.graph.nodes[args.n_id]["label_field_right"]
                    )
                ),
            ],
        ),
        var=left_data["label_text"],
    )
