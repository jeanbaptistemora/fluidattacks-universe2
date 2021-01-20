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
    core_model,
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
    dependencies: graph_model.SyntaxSteps
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]


def syntax_step_declaration(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment
    args_danger = any(
        dependency.meta.danger for dependency in args.dependencies
    )

    # Analyze if the binding itself is sensitive
    bind_danger = any((
        # This type is an HTTP request from JavaX framework
        args.syntax_step.var_type == 'HttpServletRequest',
    ))

    # Local context
    args.syntax_step.meta.danger = bind_danger or args_danger


EVALUATORS: Dict[object, Evaluator] = {
    graph_model.SyntaxStepDeclaration: syntax_step_declaration,
}


def get_dependencies(
    syntax_step_index: int,
    syntax_steps: graph_model.SyntaxSteps,
) -> graph_model.SyntaxSteps:
    dependencies: graph_model.SyntaxSteps = []
    dependencies_depth: int = 0
    dependencies_expected_length: int = (
        -syntax_steps[syntax_step_index].meta.dependencies
    )

    while len(dependencies) < dependencies_expected_length:
        syntax_step_index -= 1

        if dependencies_depth:
            dependencies_depth += 1
        else:
            dependencies.append(syntax_steps[syntax_step_index])

        dependencies_depth += syntax_steps[syntax_step_index].meta.dependencies

    return dependencies


def eval_syntax_steps(
    _: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: graph_model.NId,
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation(f'Missing Syntax Reader, {shard.path} @ {n_id}')

    syntax_steps = deepcopy(shard.syntax[n_id])

    for syntax_step_index, syntax_step in enumerate(syntax_steps):
        syntax_step_type = type(syntax_step)
        if evaluator := EVALUATORS.get(syntax_step_type):
            evaluator(EvaluatorArgs(
                dependencies=get_dependencies(syntax_step_index, syntax_steps),
                syntax_step=syntax_step,
                syntax_step_index=syntax_step_index,
                syntax_steps=syntax_steps,
            ))
        else:
            # We are not able to evaluate this step
            raise StopEvaluation(f'Missing evaluator, {syntax_step_type}')

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
        except StopEvaluation as exc:
            log_blocking('debug', str(exc))
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
    untrusted_node: core_model.FindingEnum,
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
