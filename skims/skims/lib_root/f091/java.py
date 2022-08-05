from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def get_entry_var(shard: GraphShard) -> str:
    graph = shard.graph
    for member in g.filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=g.pred_has_labels(label_type="type_identifier"),
    ):
        method_name = node_to_str(graph, member)
        if method_name == "HttpServletRequest":
            node_cfg = g.pred_ast(graph, member, depth=1)[0]
            vuln_var = g.match_ast(
                graph,
                node_cfg,
                "identifier",
            )
            vuln_var_name = node_to_str(graph, str(vuln_var["identifier"]))
            return str(vuln_var_name)
    return ""


def get_vuln_assigntion(shard: GraphShard, entry_var_name: str) -> List[str]:
    graph = shard.graph
    aux_vuln_assing = []
    for member in g.filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=g.pred_has_labels(label_type="method_invocation"),
    ):
        vuln_var = g.match_ast(
            graph,
            member,
            "identifier",
        )
        if node_to_str(graph, str(vuln_var["identifier"])) == entry_var_name:
            nicu = g.match_ast(
                graph,
                member,
                "argument_list",
            )
            nicu2 = g.match_ast(
                graph,
                str(nicu["argument_list"]),
                "string_literal",
            )
            vuln_assingnation = node_to_str(
                graph, str(nicu2["string_literal"])
            )
            aux_vuln_assing.append(vuln_assingnation)
    return aux_vuln_assing


def check_if_vuln(
    identifier: tuple, graph: Graph, vuln_assignation: str
) -> bool:
    flag = False
    for i in identifier:
        if '"' + node_to_str(graph, i) + '"' == vuln_assignation:
            flag = True
        if node_to_str(graph, i) == "replaceAll" and flag:
            return False
        if node_to_str(graph, i) == "replaceAll":
            return True
    return False


def insecure_logging(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JAVA_INSECURE_HASH

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph
            if entry_var_name := get_entry_var(shard):
                vuln_assignation1 = get_vuln_assigntion(shard, entry_var_name)

                for vuln_assignation in vuln_assignation1:
                    for member in g.filter_nodes(
                        shard.graph,
                        nodes=shard.graph.nodes,
                        predicate=g.pred_has_labels(
                            label_type="method_invocation"
                        ),
                    ):

                        bool_identifier = check_if_vuln(
                            g.adj_ast(graph, member, label_type="identifier"),
                            graph,
                            vuln_assignation,
                        )
                        if bool_identifier:
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.js_uses_console_log",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
