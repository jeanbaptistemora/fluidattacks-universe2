from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
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


def vuln_regular_expression(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_VULN_REGEX
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP
    regex_methods = {"IsMatch", "Match", "Matches"}
    rules = {"DangerousRegex"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
            ):
                if not graph.nodes[nid].get("member") in regex_methods:
                    continue
                method_id = g.pred_ast(graph, nid)[0]
                for path in get_backward_paths(graph, method_id):
                    evaluation = evaluate(method, graph, path, method_id)
                    if (
                        evaluation
                        and evaluation.danger
                        and evaluation.triggers == rules
                    ):
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def regex_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_REGEX_INJETCION
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

    def n_ids() -> graph_model.GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for member in yield_syntax_graph_member_access(graph, {"Regex"}):
                if not graph.nodes[member]["member"] == "Match":
                    continue
                pred = g.pred_ast(graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    if (
                        evaluation := evaluate(method, graph, path, pred)
                    ) and evaluation.danger:
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
