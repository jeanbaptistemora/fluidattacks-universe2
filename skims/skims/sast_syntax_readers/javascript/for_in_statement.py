from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepLoop,
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

    var_to_iterate = args.generic(
        args.fork_n_id(args.graph.nodes[args.n_id]["label_field_right"])
    )
    # A declaration is returned because in each iteration there is a variable
    # that dependends onm the iterated var
    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [var_to_iterate],
        ),
        var=left_data["label_text"],
    )
    # A loop is returned because it cloud be controlled by the user
    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [var_to_iterate],
        )
    )
