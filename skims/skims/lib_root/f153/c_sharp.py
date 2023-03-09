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
    for path in get_backward_paths(graph, n_id):
        if (evaluation := evaluate(method, graph, path, n_id)) and (
            evaluation.danger
        ):
            return True
    return False


def check_danger_arguments(graph: Graph, n_id: NId) -> bool:
    nodes = graph.nodes
    if (
        (args_n_id := nodes[n_id].get("arguments_id"))
        and (args := g.adj_ast(graph, args_n_id))
        and (len(args) > 0 and len(args) % 2 == 0)
    ):
        for index in range(0, len(args), 2):
            if (nodes[args[index]].get("value")[1:-1] == "Accept") and (
                nodes[args[index + 1]].get("value")[1:-1] == "*/*"
            ):
                return True
    return False


def get_dang_instances(
    graph: Graph,
) -> set[str]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (
                (node.get("label_type") == "VariableDeclaration")
                and (node.get("variable_type") in dang_classes)
            )
            or (
                (node.get("label_type") == "ObjectCreation")
                and (node.get("name") in dang_classes)
            )
        )

    nodes = graph.nodes
    dang_instances: set[str] = set()
    dang_classes = {"HttpClient", "HttpRequestMessage", "WebClient"}

    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if (var_name := nodes[n_id].get("variable")) or (
            (p_id := g.pred_ast(graph, n_id))
            and (v_id := nodes[p_id[0]].get("variable_id"))
            and (var_name := nodes[v_id].get("symbol"))
        ):
            dang_instances.add(var_name)

    return dang_instances


def get_dang_callings(graph: Graph) -> set[str]:
    dang_callings: set[str] = set()
    dang_invocations = {
        "DefaultRequestHeaders.Add",
        "DefaultRequestHeaders.Accept.Add",
        "Headers.Add",
        "Headers.Accept.Add",
    }
    for invocation in dang_invocations:
        for inst_name in get_dang_instances(graph):
            dang_callings.add(f"{inst_name}.{invocation}")

    return dang_callings


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> Iterator[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "MethodInvocation")
            and (node.get("expression") in dang_callings)
        )

    nodes = graph.nodes
    dang_callings = get_dang_callings(graph)
    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if (args_id := nodes[n_id].get("arguments_id")) and is_vuln(
            graph, args_id, method
        ):
            yield n_id


def c_sharp_accepts_any_mime_type(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.C_SHARP_ACCEPTS_ANY_MIMETYPE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
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
