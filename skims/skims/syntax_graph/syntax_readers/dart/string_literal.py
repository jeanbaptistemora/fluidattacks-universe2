from model.graph_model import (
    NId,
)
import re
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    pattern = re.compile(r"\$(\w*)")
    text = n_attrs["label_text"]
    template_invocations = pattern.findall(text)

    if len(template_invocations) > 0:
        return build_string_literal_node(
            args, n_attrs["label_text"], None, template_invocations
        )
    return build_string_literal_node(args, n_attrs["label_text"])
