from functools import (
    partial,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.common import (
    catch_statement as common_catch_statement,
    loop_statement as common_loop_statement,
    step_by_step as common_step_by_step,
    try_statement as common_try_statement,
)
from sast_transformations.control_flow.javascript import (
    function_declaration as javascript_function_declaration,
    if_statement as javascript_if_statement,
    switch_statement as javascript_switch_statement,
)
from sast_transformations.control_flow.types import (
    Walker,
    Walkers,
)

JAVASCRIPT = GraphShardMetadataLanguage.JAVASCRIPT


JAVASCRIPT_WALKERS: Walkers = (
    Walker(
        applicable_node_label_types={
            "statement_block",
            "expression_statement",
            "program",
        },
        walk_fun=common_step_by_step,
    ),
    Walker(
        applicable_node_label_types={
            "catch_clause",
            "finally_clause",
        },
        walk_fun=common_catch_statement,
    ),
    Walker(
        applicable_node_label_types={
            "if_statement",
        },
        walk_fun=javascript_if_statement,
    ),
    Walker(
        applicable_node_label_types={
            "function_declaration",
        },
        walk_fun=javascript_function_declaration,
    ),
    Walker(
        applicable_node_label_types={
            "switch_statement",
        },
        walk_fun=javascript_switch_statement,
    ),
    Walker(
        applicable_node_label_types={
            "try_statement",
        },
        walk_fun=partial(common_try_statement, language=JAVASCRIPT),
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "do_statement",
            "while_statement",
            "for_each_statement",
            "for_in_statement",
            "for_of_statement",
        },
        walk_fun=partial(common_loop_statement, language=JAVASCRIPT),
    ),
)
