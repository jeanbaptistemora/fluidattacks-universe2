from model import (
    graph_model,
)
from model.graph_model import (
    Graph,
    SyntaxStepIf,
    SyntaxSteps,
    SyntaxStepSymbolLookup,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Any,
    Dict,
    Iterator,
    Optional,
    Union,
)
from utils.graph import (
    adj_ast,
    adj_lazy,
)
from utils.string import (
    build_attr_paths,
)


def lookup_var_value(args: EvaluatorArgs, var_name: str) -> str:
    step_ind = 0
    for syntax_step in args.syntax_steps:
        if (
            isinstance(syntax_step, graph_model.SyntaxStepAssignment)
            and syntax_step.var == var_name
        ):
            depend = get_dependencies(step_ind, args.syntax_steps)[0]
            if isinstance(
                depend, graph_model.SyntaxStepMemberAccessExpression
            ):
                return depend.expression
            if isinstance(depend, graph_model.SyntaxStepLiteral):
                return depend.value
        step_ind += 1
    return ""


def lookup_vars(
    args: EvaluatorArgs,
) -> Iterator[
    Union[
        graph_model.SyntaxStepAssignment,
        graph_model.SyntaxStepDeclaration,
        graph_model.SyntaxStepSymbolLookup,
    ]
]:
    for syntax_step in reversed(args.syntax_steps[0 : args.syntax_step_index]):
        if isinstance(
            syntax_step,
            (
                graph_model.SyntaxStepAssignment,
                graph_model.SyntaxStepDeclaration,
                graph_model.SyntaxStepSymbolLookup,
            ),
        ):
            yield syntax_step


def lookup_var_dcl_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[
    Union[
        graph_model.SyntaxStepDeclaration,
        graph_model.SyntaxStepSymbolLookup,
    ]
]:

    vars_lookup = [
        var
        for var in lookup_vars(args)
        if isinstance(
            var,
            (
                graph_model.SyntaxStepDeclaration,
                graph_model.SyntaxStepSymbolLookup,
            ),
        )
    ]

    for syntax_step in vars_lookup:
        if (
            isinstance(syntax_step, graph_model.SyntaxStepDeclaration)
            and syntax_step.var == var_name
        ):
            return syntax_step
        # SyntaxStepDeclaration may not be vulnerable, but a later assignment
        # may be vulnerable
        if (
            isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup)
            and syntax_step.symbol == var_name
        ):
            for var in vars_lookup:
                if (
                    isinstance(var, graph_model.SyntaxStepDeclaration)
                    and var.var == var_name
                ):
                    return graph_model.SyntaxStepDeclaration(
                        meta=syntax_step.meta,
                        var=var.var,
                        var_type=var.var_type,
                    )
    return None


def lookup_var_state_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[
    Union[
        graph_model.SyntaxStepAssignment,
        graph_model.SyntaxStepDeclaration,
        graph_model.SyntaxStepSymbolLookup,
    ]
]:
    for syntax_step in lookup_vars(args):
        if (
            isinstance(
                syntax_step,
                (
                    graph_model.SyntaxStepDeclaration,
                    graph_model.SyntaxStepAssignment,
                ),
            )
            and syntax_step.var == var_name
        ) or (
            isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup)
            and syntax_step.symbol == var_name
        ):
            return syntax_step
    return None


def complete_attrs_on_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        attr: value
        for path, value in data.items()
        for attr in build_attr_paths(*path.split("."))
    }


def get_if_condition_node(graph: Graph, if_nid: str) -> list:
    if_parts = ["if", "(", ")", "block", "else"]
    return [
        c_id
        for c_id in adj_ast(graph, if_nid)
        if graph.nodes[c_id]["label_type"] not in if_parts
    ]


# Check if at least one variable is called in a method given a if statement
def var_in_method_from_if(
    args: EvaluatorArgs, if_nid: str, method: str, var_list: list
) -> bool:
    dependencies = []
    for node in list(adj_lazy(args.shard.graph, if_nid, depth=-1)):
        if args.shard.graph.nodes[node].get(
            "label_type"
        ) == "invocation_expression" and get_syntax_step_from_nid(
            args.syntax_steps, node
        ):
            s_step = get_syntax_step_from_nid(args.syntax_steps, node)
            index = list(s_step.keys()).pop()
            syntax_step = s_step[index]
            if syntax_step.method == method:
                dependencies = get_dependencies(index, args.syntax_steps)
    for depend in dependencies:
        if (
            isinstance(depend, SyntaxStepSymbolLookup)
            and depend.symbol in var_list
        ):
            return True
    return False


def get_syntax_step_from_nid(syntax_steps: SyntaxSteps, n_id: str) -> dict:
    for index, syntax_step in enumerate(syntax_steps):
        if syntax_step.meta.n_id == n_id:
            return {index: syntax_step}
    return {}


def get_dependencies_from_nid(
    syntax_steps: SyntaxSteps, n_id: str
) -> Optional[SyntaxSteps]:
    for index, syntax_step in enumerate(syntax_steps):
        if syntax_step.meta.n_id == n_id:
            return get_dependencies(index, syntax_steps)
    return None


def has_validations(
    dangers_args: list,
    args: EvaluatorArgs,
    elem_node: str,
    validation: Optional[str],
) -> bool:
    for syntax_step in args.syntax_steps:
        if (
            isinstance(syntax_step, SyntaxStepIf)
            and int(syntax_step.meta.n_id) < int(elem_node)
            and validation
        ):
            cond_nid = get_if_condition_node(
                args.shard.graph, syntax_step.meta.n_id
            )

            if len(cond_nid) > 0 and var_in_method_from_if(
                args, cond_nid[0], validation, dangers_args
            ):
                return True
    return False
