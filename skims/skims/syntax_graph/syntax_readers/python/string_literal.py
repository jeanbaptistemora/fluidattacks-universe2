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
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    text = node_to_str(graph, args.n_id)
    if text.startswith(('f"', "f'")):
        pattern = re.compile(r"\{(\w*)\}")
        template_invocations = pattern.findall(text)

        if len(template_invocations) > 0:
            return build_string_literal_node(
                args, text, None, template_invocations
            )

    return build_string_literal_node(args, text)
