from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union
)


def check_enums(
    to_check: Dict[Union[int, str, Optional[str]], List[Callable[..., Any]]]
) -> None:
    for variable, callables in to_check.items():
        if variable:
            check_to_do = callables[0]
            exception = callables[1]
            try:
                if not check_to_do(variable):
                    raise exception()
            except ValueError:
                raise exception()
