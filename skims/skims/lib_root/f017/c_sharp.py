import itertools
from lib_root.utilities.c_sharp import (
    yield_member_access,
    yield_object_creation,
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
from utils.graph.text_nodes import (
    node_to_str,
)


def verify_decoder(
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
                if node_to_str(shard.graph, member) == "decoder.Decode":
                    pred = g.pred(shard.graph, member)[0]
                    props = g.get_ast_childs(
                        shard.graph, pred, depth=4, label_type="argument"
                    )
                    if len(props) > 2 and verify_prop(shard.graph, props):
                        yield shard, member

    def verify_prop(
        graph: graph_model.GraphShard, props: Tuple[Any, ...]
    ) -> bool:
        insecure = False
        prop_value = g.match_ast(graph, props[2])["__0__"]
        if graph.nodes[prop_value].get("label_text") == "false":
            insecure = True
        elif (
            g.match_ast(graph, prop_value)
            and graph.nodes[g.match_ast(graph, prop_value)["__0__"]].get(
                "label_text"
            )
            == "verify"
        ):
            arg = g.pred(
                graph,
                prop_value,
            )[0]
            arg_value = g.get_ast_childs(
                graph, arg, label_type="boolean_literal"
            )
            if graph.nodes[arg_value[0]].get("label_text") == "false":
                insecure = True
        return insecure

    return get_vulnerabilities_from_n_ids(
        cwe=("319",),
        desc_key="F017.title",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def jwt_signed(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    object_name = {"JwtBuilder"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard, member in itertools.chain(
            yield_member_access(graph_db, object_name),
            yield_object_creation(graph_db, object_name),
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
