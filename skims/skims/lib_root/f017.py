import itertools
from lib_root.f052.c_sharp import (
    _yield_member_access as c_sharp_yield_member_access,
    _yield_object_creation as c_sharp_yield_object_creation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Any,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_member_access_expression_key,
)


def csharp_verify_decoder(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                method = build_member_access_expression_key(
                    shard.graph,
                    member,
                )
                if method == "decoder.Decode":
                    pred = g.pred(shard.graph, member)[0]
                    props = g.get_ast_childs(
                        shard.graph, pred, depth=4, label_type="identifier"
                    )
                    if not verify_prop(shard.graph, props):
                        yield shard, member

    def verify_prop(
        graph: graph_model.GraphShard, props: Tuple[Any, ...]
    ) -> bool:
        prop_value = False
        for prop in props:
            if graph.nodes[prop].get("label_text") == "verify":
                arg = g.pred(
                    graph,
                    prop,
                    depth=2,
                )[1]
                arg_value = g.get_ast_childs(
                    graph, arg, label_type="boolean_literal"
                )
                if graph.nodes[arg_value[0]].get("label_text") == "true":
                    prop_value = True
        return prop_value

    return get_vulnerabilities_from_n_ids(
        cwe=("319",),
        desc_key="F017.title",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_jwt_signed(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    object_name = {"JwtBuilder"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard, member in itertools.chain(
            c_sharp_yield_member_access(graph_db, object_name),
            c_sharp_yield_object_creation(graph_db, object_name),
        ):
            if not check_pred(shard.graph, elem_jwt=member):
                yield shard, member

    def check_pred(
        graph: graph_model.GraphShard, depth: int = 1, elem_jwt: int = 0
    ) -> bool:
        pred = g.pred(graph, elem_jwt, depth)[0]
        if graph.nodes[pred].get("label_type") == "member_access_expression":
            prop = g.get_ast_childs(graph, pred, "identifier")[0]
            if graph.nodes[prop].get("label_text") == "MustVerifySignature":
                return True
        if graph.nodes[pred].get("label_type") != "variable_declarator":
            signed = check_pred(graph, depth + 1, pred)
        else:
            return False
        return signed

    return get_vulnerabilities_from_n_ids(
        cwe=("319",),
        desc_key="F017.title",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F017
QUERIES: graph_model.Queries = (
    (FINDING, csharp_verify_decoder),
    (FINDING, csharp_jwt_signed),
)
