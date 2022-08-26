from ctx import (
    CTX,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from syntax_graph.dispatchers import (
    DISPATCHERS_BY_LANG,
)
from syntax_graph.syntax_readers.common.missing_node import (
    reader as missing_node_reader,
)
from syntax_graph.types import (
    MissingCaseHandling,
    MissingSyntaxReader,
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Optional,
)
from utils.env import (
    guess_environment,
)
from utils.logs import (
    log_blocking,
    log_to_remote_blocking,
)


def generic(args: SyntaxGraphArgs) -> str:
    node_type = args.ast_graph.nodes[args.n_id]["label_type"]

    if lang_dispatchers := DISPATCHERS_BY_LANG.get(args.language):
        for dispatcher in lang_dispatchers:
            if node_type in dispatcher.applicable_types:
                return dispatcher.syntax_reader(args)

    if guess_environment() == "production":
        log_to_remote_blocking(
            msg=f"Missing syntax reader in {args.language.name}",
            severity="warning",
            group=CTX.config.group,
            namespace=CTX.config.namespace,
            path=args.path,
            node_type=node_type,
        )

    return missing_node_reader(args, node_type)


def build_syntax_graph(
    path: str, language: GraphLanguage, ast_graph: Graph
) -> Optional[Graph]:
    try:
        syntax_graph = Graph()
        generic(
            SyntaxGraphArgs(
                generic, path, language, ast_graph, syntax_graph, "1"
            )
        )
        return syntax_graph
    except (MissingSyntaxReader, MissingCaseHandling) as error:
        log_blocking("warning", cast(str, error))
        return None
