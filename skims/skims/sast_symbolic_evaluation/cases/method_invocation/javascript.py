import functools
from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStepDeclaration,
    SyntaxStepMethodInvocation,
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


@javascript_only
def process_declaration(args: EvaluatorArgs) -> None:
    # javascript is a dynamic language the type of some
    # declarations is known at runtime
    step: SyntaxStepDeclaration = args.syntax_step
    if len(args.dependencies) == 1:
        (declaration,) = args.dependencies
        if (
            (
                args.shard.metadata.language
                == GraphShardMetadataLanguage.JAVASCRIPT
            )
            and args.syntax_step.is_destructuring
            and isinstance(declaration, SyntaxStepMethodInvocation)
        ):
            args.syntax_step.var_type = f"{declaration.return_type}.{step.var}"
