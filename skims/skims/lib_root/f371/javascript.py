from collections.abc import (
    Iterator,
)
from lib_root.f371.common import (
    has_bypass_sec,
    has_innerhtml,
    has_set_inner_html,
)
from model import (
    core_model,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def uses_innerhtml(
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_USES_INNERHTML

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            for n_id in has_innerhtml(shard.syntax_graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.generic_uses_innerhtml",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def js_bypass_security_trust_url(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_BYPASS_SECURITY_TRUST_URL

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            for n_id in has_bypass_sec(shard.syntax_graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.bypass_security_trust",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def js_dangerously_set_innerhtml(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_DANGEROUSLY_SET_HTML

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            for n_id in has_set_inner_html(shard.syntax_graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.has_dangerously_set_innerhtml",
        desc_params=dict(lang="Jsx"),
        graph_shard_nodes=n_ids(),
        method=method,
    )
