from model.graph_model import (
    SyntaxStepLoop,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    dependencies = []
    if init_id := node_attrs.get("label_field_init"):
        dependencies.append(args.generic(args.fork_n_id(init_id)))
    if condition_id := node_attrs.get("label_field_condition"):
        dependencies.append(args.generic(args.fork_n_id(condition_id)))

    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(args.n_id, dependencies),
    )
