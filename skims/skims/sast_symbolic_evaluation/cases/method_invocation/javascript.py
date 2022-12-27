from model.graph_model import (
    SyntaxStep,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def list_remove(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    dcl.meta.value.pop(index)
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_get(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    args.syntax_step.meta.value = dcl.meta.value[index]
    args.syntax_step.meta.danger = dcl.meta.value[index].meta.danger


def list_pop(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    last = dcl.meta.value.pop()
    args.syntax_step.meta.value = last.meta.value
    args.syntax_step.meta.danger = last.meta.danger
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_shift(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    firsts = dcl.meta.value.pop(0)
    args.syntax_step.meta.value = firsts.meta.value
    args.syntax_step.meta.danger = firsts.meta.danger
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_push(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    for argument in args.dependencies:
        dcl.meta.value.append(argument)
    args.syntax_step.meta.value = len(dcl.meta.value)
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_concat(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    new_list = dcl.meta.value
    for argument in args.dependencies:
        if argument.meta.value and isinstance(argument.meta.value, list):
            new_list.extend(argument.meta.value)
    args.syntax_step.meta.value = new_list
    args.syntax_step.meta.danger = any(
        x.meta.danger for x in args.syntax_step.meta.value if x
    )
