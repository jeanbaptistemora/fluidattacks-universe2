# Standard library
from typing import (
    Any,
    Callable,
    Iterator,
    Tuple,
)

# Third party libraries
from jmespath import (
    search as jsh,
)


def symbolic_evaluate(value: Any) -> Any:
    """Evaluate a list of expressions, return a possibly simplified equivalent.

    Examples:

        >>> [StringLiteral, ADD, StringLiteral, ADD, StringLiteral]
        StringLiteral
    """
    # Only a list of expressions can be evaluated
    if not isinstance(value, list):
        return value

    # Recursively simplify the element
    value = list(map(symbolic_evaluate, value))

    # Value is composed from 'StringLiterals' joined by 'ADD'
    if set(jsh('[0::2].type', value)) == {'StringLiteral'} \
            and set(jsh('[1::2].type', value)) == {'ADD'}:
        final = value[0]
        final['text'] = '"' + ''.join(t['text'][1:-1] for t in value) + '"'
        return final

    return value


def simplify(value: Any) -> Any:
    """Access single node elements in order to flatten a graph.

    Examples:

        >>> simplify([{'a': 1}]) == {'a': 1}

        >>> simplify({'a': []}) == []
    """
    if isinstance(value, list):
        if len(value) == 1:
            return simplify(value[0])
        return list(map(simplify, value))

    if isinstance(value, dict):
        if len(value) == 1:
            child_val, = value.values()
            return simplify(child_val)
        return dict(zip(value.keys(), map(simplify, value.values())))

    return value


def yield_nodes(
    *,
    key: str = '__root__',
    value: Any,
    key_predicates: Tuple[Callable[[str], bool], ...] = (),
    value_extraction: str = '@',
    value_predicates: Tuple[str, ...] = (),
    post_actions: Tuple[Callable[[Any], Any], ...] = (
        simplify,
        symbolic_evaluate,
    ),
) -> Iterator[Any]:
    """Recursively scan the graph and yield nodes that match the predicates."""

    def _yield_if_matches() -> Iterator[Any]:
        if all(jsh(pred, value) for pred in value_predicates) \
                and all(pred(key) for pred in key_predicates):
            to_yield = jsh(value_extraction, value)
            for post_action in post_actions:
                to_yield = post_action(to_yield)
            yield to_yield

    if isinstance(value, dict):
        yield from _yield_if_matches()
        for child_key, child_value in value.items():
            yield from yield_nodes(
                key=child_key,
                value=child_value,
                key_predicates=key_predicates,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )
    elif isinstance(value, list):
        yield from _yield_if_matches()
        for child_key, child_value in enumerate(value):
            yield from yield_nodes(
                key=f'{key}[{child_key}]',
                value=child_value,
                key_predicates=key_predicates,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )
