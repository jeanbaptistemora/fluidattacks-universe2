from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepObjectInstantiation,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match_pairs = g.match_ast_group(args.graph, args.n_id, "pair")
    current_object = {}
    for pair_id in match_pairs["pair"]:
        pair_attrs = args.graph.nodes[pair_id]
        key_name = args.graph.nodes[pair_attrs["label_field_key"]][
            "label_text"
        ]
        value = args.generic(args.fork_n_id(pair_attrs["label_field_value"]))
        current_object[key_name] = value[-1]

    yield SyntaxStepObjectInstantiation(
        meta=SyntaxStepMeta(
            danger=False,
            dependencies=[list(current_object.values())],
            n_id=args.n_id,
            value=current_object,
        ),
        object_type="object",
    )
