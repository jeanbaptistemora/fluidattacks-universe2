from lib_root.f052 import (
    _csharp_yield_member_access,
    _csharp_yield_object_creation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def csharp_jwt_signed(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    object_name = {"JwtBuilder"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            members_jwt = list(
                _csharp_yield_member_access(graph_db, object_name)
            )
            object_jwt = list(
                _csharp_yield_object_creation(graph_db, object_name)
            )

            object_jwt += members_jwt

            for element in object_jwt:
                if not check_pred(shard.graph, elem_jwt=element[1]):
                    yield shard, element[1]

    def check_pred(
        graph: graph_model.GraphShard, depth: int = 1, elem_jwt: int = 0
    ) -> bool:
        pred = g.pred(graph, elem_jwt, depth)
        print(pred[0])
        if (
            graph.nodes[pred[0]].get("label_type")
            == "member_access_expression"
        ):
            prop = g.get_ast_childs(graph, pred[0], "identifier")
            if graph.nodes[prop[0]].get("label_text") == "MustVerifySignature":
                return True
        if graph.nodes[pred[0]].get("label_type") != "variable_declaration":
            signed = check_pred(graph, depth + 1, pred[0])
        else:
            signed = False
        return signed

    return get_vulnerabilities_from_n_ids(
        cwe=("319",),
        desc_key="F017.title",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F017
QUERIES: graph_model.Queries = ((FINDING, csharp_jwt_signed),)
