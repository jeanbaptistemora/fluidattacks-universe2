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


def generic(args: SyntaxGraphArgs) -> str:
    node_type = args.ast_graph.nodes[args.n_id]["label_type"]

    for dispatcher in DISPATCHERS_BY_LANG[args.language]:
        if node_type in dispatcher.applicable_types:
            return dispatcher.syntax_reader(args)

    raise MissingSyntaxReader(
        f"Missing syntax reader for {node_type} in {args.language.name}"
    )


def build_syntax_graph(
    language: GraphLanguage, ast_graph: Graph
) -> Optional[Graph]:
    if language not in DISPATCHERS_BY_LANG:
        return None

    try:
        syntax_graph = Graph()
        generic(
            SyntaxGraphArgs(generic, language, ast_graph, syntax_graph, "1")
        )
        return syntax_graph
    except (MissingSyntaxReader, MissingCaseHandling) as error:
        print(error)
        return None
