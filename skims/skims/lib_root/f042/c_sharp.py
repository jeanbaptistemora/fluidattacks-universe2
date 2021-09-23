from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def c_sharp_check_cookie_security(
    shard: graph_model.GraphShard, checks: Set[str], name_var: str
) -> int:
    count_checks = 0
    for syntax_steps in shard.syntax.values():
        *dependencies, syntax_step = syntax_steps

        if syntax_step.type != "SyntaxStepAssignment":
            continue

        # this funcion search for var.attribute = true
        # so it should only have 1 dependency, the boolean value
        if len(dependencies) != 1:
            continue

        dep = dependencies[0]
        if dep.type != "SyntaxStepLiteral" or dep.value != "true":
            continue

        var, attribute = syntax_step.var.split(".", maxsplit=1)
        if var == name_var and attribute in checks:
            count_checks += 1

    return count_checks


def insecurely_generated_cookies(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:

    security_props = {
        "HttpOnly",
        "Secure",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="object_creation_expression"
                ),
            ):
                match_object_creation = g.match_ast(
                    shard.graph, member, "__0__"
                )
                name_var = shard.graph.nodes[
                    g.match_ast(
                        shard.graph, g.pred(shard.graph, member, 2)[1], "__0__"
                    )["__0__"]
                ].get("label_text")
                if (
                    shard.graph.nodes[match_object_creation["__1__"]].get(
                        "label_text"
                    )
                    == "HttpCookie"
                ) and (
                    c_sharp_check_cookie_security(
                        shard, security_props, name_var
                    )
                    != len(security_props)
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("614",),
        desc_key="F042.description",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F042
