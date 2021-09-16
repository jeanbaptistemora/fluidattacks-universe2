from itertools import (
    chain,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
    Vulnerability,
)
from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    shard_n_id_query,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from sast_transformations.danger_nodes.utils import (
    append_label_input,
    mark_methods_sink,
)
from typing import (
    Iterator,
)
from utils.languages.javascript import (
    is_cipher_vulnerable as javascript_cipher_vulnerable,
)
from utils.string import (
    split_on_last_dot,
)


def insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def find_vulns(
        shard: GraphShard,
    ) -> Iterator[Vulnerability]:
        for syntax_steps in shard.syntax.values():
            for index, invocation_step in enumerate(syntax_steps):
                if invocation_step.type != "SyntaxStepMethodInvocation":
                    continue
                _, method = split_on_last_dot(invocation_step.method)
                if method not in {"createCipheriv", "createDecipheriv"}:
                    continue
                dependencies = get_dependencies(index, syntax_steps)
                algorithm = dependencies[-1]
                if (
                    # pylint: disable=used-before-assignment
                    algorithm.type == "SyntaxStepLiteral"
                    and (algorithm_value := algorithm.value)
                    and javascript_cipher_vulnerable(algorithm_value)
                ):
                    yield get_vulnerabilities_from_n_ids(
                        cwe=("310", "327"),
                        desc_key=(
                            "src.lib_path.f052.insecure_cipher.description"
                        ),
                        desc_params=dict(lang="JavaScript"),
                        finding=FINDING,
                        graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
                    )
                elif algorithm.type == "SyntaxStepSymbolLookup":
                    append_label_input(shard.graph, "1", FINDING)
                    mark_methods_sink(
                        FINDING,
                        shard.graph,
                        shard.syntax,
                        {"createCipheriv", "createDecipheriv"},
                    )
                    yield shard_n_id_query(graph_db, FINDING, shard, "1")

    return tuple(
        chain.from_iterable(
            chain.from_iterable(find_vulns(shard))
            for shard in graph_db.shards_by_language(
                GraphShardMetadataLanguage.JAVASCRIPT
            )
        )
    )


FINDING: FindingEnum = FindingEnum.F052
