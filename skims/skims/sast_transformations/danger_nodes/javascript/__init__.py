# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphSyntax,
)
from sast_transformations.danger_nodes.javascript import (
    express,
)
from sast_transformations.danger_nodes.utils import (
    mark_methods_sink,
)


def mark_sinks(
    graph: Graph,
    syntax: GraphSyntax,
) -> None:
    mark_methods_sink(
        FindingEnum.F004,
        graph,
        syntax,
        {
            "exec",
            "execSync",
        },
    )
    mark_methods_sink(
        FindingEnum.F112,
        graph,
        syntax,
        {
            "query",
        },
    )
    mark_methods_sink(
        FindingEnum.F008,
        graph,
        syntax,
        {
            "send",
        },
    )
    mark_methods_sink(
        FindingEnum.F042,
        graph,
        syntax,
        {
            "cookie",
        },
    )
    mark_methods_sink(
        FindingEnum.F021,
        graph,
        syntax,
        {
            "select",
        },
    )
    mark_methods_sink(
        FindingEnum.F063,
        graph,
        syntax,
        {
            "readFile",
            "readFileSync",
            "unlink",
            "unlinkSync",
            "writeFile",
            "writeFileSync",
            "readdir",
            "readdirSync",
            "exist",
            "existSync",
            "rmdir",
            "rmdirSync",
            "stat",
            "statSync",
            "appendFile",
            "appendFileSync",
            "chown",
            "chownSync",
            "chmod",
            "chmodSync",
            "copyFile",
            "copyFileSync",
            "createReadStream",
            "createWriteStream",
            "exists",
            "existsSync",
        },
    )


def mark_inputs(
    graph: Graph,
    syntax: GraphSyntax,
) -> None:
    express.mark_requests(graph, syntax)
