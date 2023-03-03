from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def get_suspicious_nodes(
    graph: Graph, dang_invocations: set[str]
) -> Iterator[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "MethodInvocation")
            and (node.get("expression") in dang_invocations)
        )

    for n_id in g.filter_nodes(graph, graph.nodes, predicate_matcher):
        yield n_id


def check_danger_arguments(graph: Graph, n_id: NId) -> bool:
    nodes = graph.nodes
    return bool(
        (args_n_id := nodes[n_id].get("arguments_id"))
        and (args := g.adj_ast(graph, args_n_id))
        and (len(args) == 2)
        and (nodes[args[0]].get("value")[1:-1] == "Accept")
        and (nodes[args[1]].get("value")[1:-1] == "*/*")
    )


def is_vuln_plain(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    dang_triggers: set[str] = {"all_myme_types_allowed"}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == dang_triggers
        ):
            return True
    return False


def is_vuln_chain(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)

        if evaluation and evaluation.danger:
            return True
    return False


def get_vuln_nodes_plain(
    graph: Graph, method: MethodsEnum, dang_invocations: set[str]
) -> Iterator[NId]:

    for n_id in get_suspicious_nodes(graph, dang_invocations):
        if is_vuln_plain(graph, n_id, method):
            yield n_id

    for n_id in g.matching_nodes(
        graph, label_type="ObjectCreation", name="Header"
    ):
        if check_danger_arguments(graph, n_id):
            yield n_id


def get_vuln_nodes_chain(
    graph: Graph, method: MethodsEnum, dang_invocations: set[str]
) -> Iterator[NId]:
    for n_id in get_suspicious_nodes(graph, dang_invocations):
        if check_danger_arguments(graph, n_id) and is_vuln_chain(
            graph, n_id, method
        ):
            yield n_id


def java_http_accepts_any_mime_type(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in get_vuln_nodes_plain(graph, method, dang_invocations):
                yield shard, n_id

    method = MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MIMETYPE

    dang_invocations: set[str] = {
        "setRequestProperty",
        "header",
        "setHeader",
        "addHeader",
        "add",
    }

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_accepts_any_mime_type_chain(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_ACCEPTS_ANY_MIMETYPE_CHAIN

    dang_invocations: set[str] = {
        "header",
        "setHeader",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in get_vuln_nodes_chain(graph, method, dang_invocations):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
