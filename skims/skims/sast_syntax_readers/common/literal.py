from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    n_attrs = args.graph.nodes[args.n_id]
    n_attrs_label_type = n_attrs["label_type"]

    if n_attrs_label_type in {
        "decimal_integer_literal",
        "integer_literal",
        "real_literal",
    }:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="number",
        )
    elif n_attrs_label_type in {"false", "true", "boolean_literal"}:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="boolean",
        )
    elif n_attrs_label_type == "null_literal":
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="null",
        )
    elif n_attrs_label_type in {
        "character_literal",
        "string_literal",
        "verbatim_string_literal",
    }:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"][1:-1],
            value_type="string",
        )
    else:
        raise MissingCaseHandling(args)
