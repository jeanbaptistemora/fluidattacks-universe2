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


def is_vuln(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
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


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> Iterator[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "MethodInvocation")
            and (node.get("expression") in dang_invocations)
        )

    dang_invocations: set[str] = {"setRequestProperty", "header", "setHeader"}

    for n_id in g.filter_nodes(graph, graph.nodes, predicate_matcher):
        if is_vuln(graph, n_id, method):
            yield n_id


def java_http_accepts_any_myme_type(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MYMETYPE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in get_vuln_nodes(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
