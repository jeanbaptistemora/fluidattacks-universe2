# Standard library
from copy import (
    deepcopy,
)
from typing import (
    Callable,
    Dict,
    NamedTuple,
    Tuple,
)
from model import (
    graph_model,
)
from utils import (
    graph as g,
)
from utils.logs import (
    log_blocking,
)


class StopEvaluation(Exception):
    pass


class EvaluatorArgs(NamedTuple):
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]


EVALUATORS: Dict[object, Evaluator] = {
}


def eval_syntax_steps(
    _: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: graph_model.NId,
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation()

    syntax_steps = deepcopy(shard.syntax[n_id])

    for syntax_step in syntax_steps:
        if evaluator := EVALUATORS.get(type(syntax_step)):
            evaluator(EvaluatorArgs(
                syntax_steps=syntax_steps,
            ))
        else:
            # We are not able to evaluate this step
            raise StopEvaluation()

    # Mark steps as dangerous or not
    #
    # If needed this can extend the syntax steps to be longer
    # for instance in a method invocation
    #
    # Pending to implement

    return syntax_steps


def get_syntax_steps_from_path(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    path: Tuple[str, ...],
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    for n_id in path:
        try:
            syntax_steps.extend(eval_syntax_steps(
                _=graph_db,
                shard=shard,
                n_id=n_id,
            ))
        except StopEvaluation:
            log_blocking('debug', 'SymEval stopped, %s @ %s', shard.path, n_id)
            break

    return syntax_steps


def from_untrusted_n_id_to_dangerous_action_node(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    *,
    untrusted_n_id: graph_model.NId,
) -> graph_model.GraphShardNodes:
    # Find paths from this node to all CFG connected leaf-nodes
    for _, path in g.branches_cfg(shard.graph, untrusted_n_id):
        syntax_steps = get_syntax_steps_from_path(graph_db, shard, path)

        # Check here if the syntax steps returned contain danger in the
        # dangerous_action_node. Temporarily never happens
        if '__never__' in syntax_steps:
            yield shard, g.ROOT_NODE


def from_untrusted_node_to_dangerous_action_node(
    graph_db: graph_model.GraphDB,
    *,
    untrusted_node: graph_model.GraphUntrustedNode,
) -> graph_model.GraphShardNodes:
    # Start the evaluation from the untrusted nodes, in any shard
    for shard in graph_db.shards:
        for untrusted_n_id in g.filter_nodes(
            shard.graph,
            shard.graph.nodes,
            predicate=g.pred_has_labels(label_input_type=untrusted_node.value),
        ):
            yield from from_untrusted_n_id_to_dangerous_action_node(
                graph_db,
                shard=shard,
                # We start evaluation at the CFG-connected nodes
                untrusted_n_id=g.lookup_first_cfg_parent(
                    shard.graph,
                    untrusted_n_id,
                ),
            )
