# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
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
    List,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.string import (
    split_on_last_dot,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def get_vuln_nodes(graph: Graph) -> List[str]:
    method = MethodsEnum.JS_XML_PARSER
    vuln_nodes: List[str] = []
    for nid in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        f_name: Tuple[str, str] = split_on_last_dot(
            graph.nodes[nid]["expression"]
        )
        if f_name[-1] == "parseXmlString":
            if args := g.match_ast_d(graph, nid, "ArgumentList"):
                childs = g.adj_ast(graph, args)
                if len(childs) > 1 and get_eval_danger(
                    graph, childs[1], method
                ):
                    vuln_nodes.append(nid)

    return vuln_nodes


def xml_parser(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_XML_PARSER

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            for n_id in get_vuln_nodes(shard.syntax_graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.js_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
