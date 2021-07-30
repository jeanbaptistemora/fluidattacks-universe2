from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepObjectInstantiation,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match_pairs = g.match_ast_group(args.graph, args.n_id, "pair")
    current_object = dict()
    for pair_id in match_pairs["pair"]:
        match = g.match_ast(
            args.graph, pair_id, "property_identifier", ":", "__0__"
        )
        key_name_id = match["property_identifier"]
        if not key_name_id:
            raise MissingCaseHandling(args)
        key_name = args.graph.nodes[key_name_id]["label_text"]
        current_object[key_name] = args.generic(args.fork_n_id(match["__0__"]))

    yield SyntaxStepObjectInstantiation(
        meta=SyntaxStepMeta(
            danger=False, dependencies=[], n_id=args.n_id, value=current_object
        ),
        object_type="object",
    )
