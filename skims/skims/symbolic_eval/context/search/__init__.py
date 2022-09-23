# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.context.search import (
    assignment,
    call_expression,
    class_body,
    declaration_block,
    for_each,
    if_statement,
    method_declaration,
    method_invocation,
    using_statement,
    variable_declaration,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    Searcher,
    SearchResult,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Dict,
    Iterator,
    Optional,
)

SEARCHERS: Dict[str, Searcher] = {
    "Assignment": assignment.search,
    "CallExpression": call_expression.search,
    "ClassBody": class_body.search,
    "DeclarationBlock": declaration_block.search,
    "ForEachStatement": for_each.search,
    "If": if_statement.search,
    "MethodDeclaration": method_declaration.search,
    "MethodInvocation": method_invocation.search,
    "UsingStatement": using_statement.search,
    "VariableDeclaration": variable_declaration.search,
}


def search(
    graph: Graph, path: Path, symbol: str, def_only: bool
) -> Iterator[SearchResult]:
    for n_id in path:
        if searcher := SEARCHERS.get(graph.nodes[n_id]["label_type"]):
            yield from searcher(SearchArgs(graph, n_id, symbol, def_only))


def search_until_def(graph: Graph, path: Path, symbol: str) -> Iterator[NId]:
    for is_def, ref_id in search(graph, path, symbol, def_only=False):
        yield ref_id
        if is_def:
            break


def definition_search(graph: Graph, path: Path, symbol: str) -> Optional[NId]:
    for _, ref_id in search(graph, path, symbol, def_only=True):
        return ref_id
    return None
