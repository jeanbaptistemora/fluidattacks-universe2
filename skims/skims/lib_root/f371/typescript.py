# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f371.common import (
    has_innerhtml,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)


def uses_innerhtml(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.TS_USES_INNERHTML

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            yield from has_innerhtml(shard)

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.generic_uses_innerhtml",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )