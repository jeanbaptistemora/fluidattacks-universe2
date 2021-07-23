from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    n_attrs = args.graph.nodes[args.n_id]
    n_attrs_label_type = n_attrs["label_type"]

    if n_attrs_label_type in {
        "decimal_integer_literal",
        "int_literal",
        "integer_literal",
        "number",
        "real_literal",
    }:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="number",
        )
    elif n_attrs_label_type in {"composite_literal"}:
        value_type: str = ""
        if (
            args.graph.nodes[n_attrs["label_field_type"]]["label_type"]
            == "qualified_type"
        ):
            value_type = g.concatenate_label_text(
                args.graph, g.adj_ast(args.graph, n_attrs["label_field_type"])
            )
        elif "label_text" in args.graph.nodes[n_attrs["label_field_type"]]:
            value_type = g.concatenate_label_text(
                args.graph, (n_attrs["label_field_type"],)
            )
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value={},
            value_type=f"struct[{value_type}]",
        )
    elif n_attrs_label_type in {"false", "true", "boolean_literal"}:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="boolean",
        )
    elif n_attrs_label_type in {"nil", "null_literal"}:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"],
            value_type="null",
        )
    elif n_attrs_label_type in {
        "character_literal",
        "interpreted_string_literal",
        "raw_string_literal",
        "string_literal",
        "verbatim_string_literal",
        "string",
    }:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs["label_text"][1:-1],
            value_type="string",
        )
    else:
        raise MissingCaseHandling(args)
