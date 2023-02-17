from ctx import (
    CTX,
)
from model import (
    core_model,
    graph_model,
)
import os
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)


def get_vulnerability_from_n_id(
    *,
    desc_key: str,
    desc_params: dict[str, str],
    graph_shard: graph_model.GraphShard,
    n_id: str,
    method: core_model.MethodsEnum,
    metadata: dict[str, Any] | None = None,
) -> core_model.Vulnerability:
    # Root -> meta -> file graph
    what_data = meta_attrs_label_path = graph_shard.path

    n_attrs: graph_model.NAttrs = graph_shard.graph.nodes[n_id]
    n_attrs_label_column = n_attrs["label_c"]
    n_attrs_label_line = n_attrs["label_l"]

    with open(
        file=os.path.join(CTX.config.working_dir, meta_attrs_label_path),
        encoding="latin-1",
    ) as handle:
        content: str = handle.read()

    if metadata:
        what_data = (
            f"{meta_attrs_label_path} ({meta_what})"
            if (meta_what := metadata.get("what"))
            else what_data
        )
        desc_params = (
            meta_desc_params
            if (meta_desc_params := metadata.get("desc_params"))
            else desc_params
        )

    return build_lines_vuln(
        method=method,
        what=what_data,
        where=str(n_attrs_label_line),
        metadata=build_metadata(
            method=method,
            description=(
                f"{t(key=desc_key, **desc_params)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{meta_attrs_label_path}"
            ),
            snippet=make_snippet(
                content=content,
                viewport=SnippetViewport(
                    column=int(n_attrs_label_column),
                    line=int(n_attrs_label_line),
                ),
            ).content,
        ),
    )


def get_vulnerabilities_from_n_ids_metadata(
    *,
    desc_key: str,
    desc_params: dict[str, str],
    graph_shard_nodes: graph_model.MetadataGraphShardNodes,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:

    return tuple(
        get_vulnerability_from_n_id(
            desc_key=desc_key,
            desc_params=desc_params,
            graph_shard=graph_shard,
            n_id=n_id,
            method=method,
            metadata=metadata,
        )
        for graph_shard, n_id, metadata in graph_shard_nodes
    )


def get_vulnerabilities_from_n_ids(
    *,
    desc_key: str,
    desc_params: dict[str, str],
    graph_shard_nodes: graph_model.GraphShardNodes,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        get_vulnerability_from_n_id(
            desc_key=desc_key,
            desc_params=desc_params,
            graph_shard=graph_shard,
            n_id=n_id,
            method=method,
        )
        for graph_shard, n_id in graph_shard_nodes
    )
