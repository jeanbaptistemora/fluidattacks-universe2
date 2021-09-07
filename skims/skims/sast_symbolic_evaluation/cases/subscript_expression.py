from contextlib import (
    suppress,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    StopEvaluation,
)


def evaluate(args: EvaluatorArgs) -> None:
    if len(args.dependencies) != 2:
        raise StopEvaluation.from_args(args)

    _key, _object = args.dependencies
    if (
        # pylint: disable=used-before-assignment
        (_value_dict := _object.meta.value)
        and isinstance(_value_dict, dict)
        and (key_str := _key.meta.value)
        and (_value := _value_dict.get(key_str))
    ):
        args.syntax_step.meta.value = _value.meta.value
        args.syntax_step.meta.danger = _value.meta.danger
    elif (
        (_value_list := _object.meta.value)
        and isinstance(_value_dict, list)
        and (index_str := _key.meta.value)
    ):
        with suppress(IndexError, ValueError):
            _value = _value_list[int(index_str)]
            args.syntax_step.meta.value = _value.meta.value
            args.syntax_step.meta.danger = _value.meta.danger
    else:
        args.syntax_step.meta.value = args.dependencies[1].meta.value
        args.syntax_step.meta.danger = _object.meta.danger
