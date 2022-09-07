# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage,
    NId,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, ";")

    if (
        len(match) == 2 and match[";"]
    ) or args.language == GraphShardMetadataLanguage.JAVASCRIPT:
        expression_id = match["__0__"]
        return args.generic(args.fork_n_id(str(expression_id)))

    raise MissingCaseHandling(f"Bad expression handling in {args.n_id}")
