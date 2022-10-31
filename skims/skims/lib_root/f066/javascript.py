# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f066.common import (
    n_ids_uses_console_fns,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def js_uses_console_log(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_CONSOLE_LOG

    n_ids_uses_console_fns(graph_db, GraphLanguage.JAVASCRIPT)

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.generic_uses_console_log",
        desc_params=dict(lang="Javascript"),
        graph_shard_nodes=n_ids_uses_console_fns(
            graph_db, GraphLanguage.JAVASCRIPT
        ),
        method=method,
    )
