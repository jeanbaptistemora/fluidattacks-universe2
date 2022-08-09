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
        method_name = str(node_to_str(graph, member))
        if method_name == "HttpServletRequest":
            node_cfg = g.pred_ast(graph, member, depth=1)[0]
            vuln_var = g.match_ast(
                graph,
                node_cfg,
                "identifier",
            )
            vuln_var_name = str(
                node_to_str(graph, str(vuln_var["identifier"]))
            )
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
        if (
            str(node_to_str(graph, str(vuln_var["identifier"])))
            == entry_var_name
        ):
            nicu = g.pred_ast(
                graph,
                member,
            )
            if (
                graph.nodes[nicu[0]].get("label_type", "")
                == "variable_declarator"
            ):
                nicu2 = g.match_ast(
                    graph,
                    nicu[0],
                    "identifier",
                )
                vuln_assingnation = node_to_str(
                    graph, str(nicu2["identifier"])
                )
                aux_vuln_assing.append(vuln_assingnation)
    return aux_vuln_assing


def get_vuln_vars(
    identifier: tuple, graph: Graph, vuln_assignation: List[str]
) -> List[str]:
    flag = False
    for i in identifier:
        if node_to_str(graph, i) in vuln_assignation:
            flag = True
            var_vuln_name = node_to_str(graph, i)
        if node_to_str(graph, i) == "replaceAll" and flag:
            if (
                node_to_str(
                    graph,
                    str(
                        g.match_ast(
                            graph,
                            str(g.pred_ast(graph, i, depth=2)[1]),
                            "identifier",
                        )["identifier"]
                    ),
                )
                == var_vuln_name
            ):
                vuln_assignation.remove(var_vuln_name)
    return vuln_assignation


def check_if_vuln(graph: Graph, vulnm: List[str], identifier: tuple) -> bool:
    for i in identifier:
        if node_to_str(graph, i) in vulnm:
            return True
    return False


def insecure_logging(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JAVA_INSECURE_LOGGING

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph
            if entry_var_name := get_entry_var(shard):
                vuln_assignation1 = get_vuln_assigntion(shard, entry_var_name)
                for member in g.filter_nodes(
                    shard.graph,
                    nodes=shard.graph.nodes,
                    predicate=g.pred_has_labels(
                        label_type="method_invocation"
                    ),
                ):
                    vulnm = get_vuln_vars(
                        g.adj_ast(
                            graph,
                            member,
                            label_type="identifier",
                        ),
                        graph,
                        vuln_assignation1,
                    )

                    if node_to_str(graph, member).startswith("Logger.info"):

                        if check_if_vuln(
                            graph,
                            vulnm,
                            g.adj_ast(
                                graph,
                                member,
                                depth=-1,
                                label_type="identifier",
                            ),
                        ):
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
