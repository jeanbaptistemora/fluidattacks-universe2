from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_argument_vuln(
    graph: Graph,
    n_id: NId,
) -> bool:
    method = MethodsEnum.JAVA_UNSAFE_XSS_CONTENT
    danger_set = {"userconnection", "userresponse"}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == danger_set:
            return True
    return False


def remote_command_execution(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    java = GraphLanguage.JAVA
    danger_methods = {"format", "write", "println", "printf"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                n_attrs = graph.nodes[n_id]
                m_name = n_attrs["expression"]
                obj_id = n_attrs.get("object_id")
                if (
                    m_name in danger_methods
                    and obj_id
                    and graph.nodes[obj_id].get("expression") == "getWriter"
                    and is_argument_vuln(graph, n_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_UNSAFE_XSS_CONTENT,
    )
