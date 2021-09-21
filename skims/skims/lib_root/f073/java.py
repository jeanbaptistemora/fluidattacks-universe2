from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)


def switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            for syntax_steps in shard.syntax.values():
                for index, syntax_step in enumerate(syntax_steps):
                    if isinstance(syntax_step, graph_model.SyntaxStepSwitch):
                        cases = get_dependencies(index, syntax_steps)[1:]
                        has_default = any(
                            isinstance(
                                case, graph_model.SyntaxStepSwitchLabelDefault
                            )
                            for case in cases
                        )
                        if not has_default:
                            yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
