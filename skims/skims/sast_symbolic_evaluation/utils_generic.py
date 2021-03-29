# Standard library
from typing import (
    Iterator,
    Optional,
    Union,
)

# Local libraries
from model import (
    graph_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def lookup_vars(args: EvaluatorArgs) -> Iterator[Union[
    graph_model.SyntaxStepAssignment,
    graph_model.SyntaxStepDeclaration,
    graph_model.SyntaxStepSymbolLookup,
]]:
    for syntax_step in reversed(args.syntax_steps[0:args.syntax_step_index]):
        if isinstance(syntax_step, (
            graph_model.SyntaxStepAssignment,
            graph_model.SyntaxStepDeclaration,
            graph_model.SyntaxStepSymbolLookup,
        )):
            yield syntax_step


def lookup_var_dcl_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[Union[
    graph_model.SyntaxStepDeclaration,
    graph_model.SyntaxStepSymbolLookup,
]]:

    vars_lookup = [
        var
        for var in lookup_vars(args)
        if isinstance(var, (
            graph_model.SyntaxStepDeclaration,
            graph_model.SyntaxStepSymbolLookup,
        ))
    ]

    for syntax_step in vars_lookup:
        if isinstance(syntax_step, graph_model.SyntaxStepDeclaration
                      ) and syntax_step.var == var_name:
            return syntax_step
        # SyntaxStepDeclaration may not be vulnerable, but a later assignment
        # may be vulnerable
        if isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup
                      ) and syntax_step.symbol == var_name:
            for var in vars_lookup:
                if isinstance(var, graph_model.SyntaxStepDeclaration
                              ):
                    if var.var == var_name:
                        return graph_model.SyntaxStepDeclaration(
                            meta=syntax_step.meta,
                            var=var.var,
                            var_type=var.var_type)
    return None


def lookup_var_state_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[Union[
    graph_model.SyntaxStepAssignment,
    graph_model.SyntaxStepDeclaration,
    graph_model.SyntaxStepSymbolLookup,
]]:
    for syntax_step in lookup_vars(args):
        if (isinstance(syntax_step, (
                graph_model.SyntaxStepDeclaration,
                graph_model.SyntaxStepAssignment,
        )) and syntax_step.var == var_name) or (
                isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup)
                and syntax_step.symbol == var_name):
            return syntax_step
    return None
