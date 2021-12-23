from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from syntax_graph.dispatchers import (
    DISPATCHERS_BY_LANG,
)
from syntax_graph.types import (
    MissingCaseHandling,
    MissingSyntaxReader,
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)
from utils.logs import (
    log_blocking,
)


def generic(args: SyntaxGraphArgs) -> str:
    node_type = args.ast_graph.nodes[args.n_id]["label_type"]

    if lang_dispatchers := DISPATCHERS_BY_LANG.get(args.language):
        for dispatcher in lang_dispatchers:
            if node_type in dispatcher.applicable_types:
                return dispatcher.syntax_reader(args)

    raise MissingSyntaxReader(
        f"Missing syntax reader for {node_type} in {args.language.name}"
    )


def build_syntax_graph(
    language: GraphLanguage, ast_graph: Graph
) -> Optional[Graph]:
    try:
        syntax_graph = Graph()
        generic(
            SyntaxGraphArgs(generic, language, ast_graph, syntax_graph, "1")
        )
        return syntax_graph
    except (MissingSyntaxReader, MissingCaseHandling) as error:
        log_blocking("warning", error)
        return None
