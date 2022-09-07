# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
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
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def verify_decoder(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_VERIFY_DECODER

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            objects_jwt = get_object_identifiers(graph, {"JwtDecoder"})

            for member in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
            ):
                exp = graph.nodes[member]["expression"]
                memb = graph.nodes[member]["member"]
                if (
                    exp in objects_jwt
                    and memb == "Decode"
                    and (
                        al_id := graph.nodes[g.pred(graph, member)[0]].get(
                            "arguments_id"
                        )
                    )
                    and (test_nid := g.match_ast(graph, al_id).get("__2__"))
                ):
                    for path in get_backward_paths(graph, test_nid):
                        evaluation = evaluate(method, graph, path, test_nid)
                        if evaluation and evaluation.danger:
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def jwt_signed(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP
    method = core_model.MethodsEnum.CS_JWT_SIGNED
    object_name = {"JwtBuilder"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph

            for member in [
                *yield_syntax_graph_member_access(graph, object_name),
                *yield_syntax_graph_object_creation(graph, object_name),
            ]:
                if not check_pred(graph, elem_jwt=member):
                    yield shard, member

    def check_pred(
        graph: graph_model.Graph, depth: int = 1, elem_jwt: str = "0"
    ) -> bool:
        pred = g.pred(graph, elem_jwt, depth)[0]
        if (
            graph.nodes[pred].get("label_type") == "MemberAccess"
            and graph.nodes[pred].get("member") == "MustVerifySignature"
        ):
            return True
        if graph.nodes[pred].get("label_type") != "VariableDeclaration":
            signed = check_pred(graph, depth + 1, pred)
        else:
            return False
        return signed

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
