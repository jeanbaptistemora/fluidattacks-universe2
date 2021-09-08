import functools
from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from typing import (
    Callable,
    Optional,
)

TFun = Callable[[EvaluatorArgs], None]


def javascript_only(
    func: TFun,
) -> Callable[[EvaluatorArgs], Optional[TFun]]:
    @functools.wraps(func)
    def wrapper_decorator(args: EvaluatorArgs) -> Optional[TFun]:
        if (
            args.shard.metadata.language
            != GraphShardMetadataLanguage.JAVASCRIPT
        ):
            return None
        return func(args)

    return wrapper_decorator


def go_only(
    func: TFun,
) -> Callable[[EvaluatorArgs], Optional[TFun]]:
    @functools.wraps(func)
    def wrapper_decorator(args: EvaluatorArgs) -> Optional[TFun]:
        if args.shard.metadata.language != GraphShardMetadataLanguage.GO:
            return None
        return func(args)

    return wrapper_decorator
