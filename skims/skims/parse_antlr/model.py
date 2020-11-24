# Standard library
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from parse_antlr.common import (
    is_positional_node,
)


def _parse_rule(model: List[Dict[str, Any]]) -> Dict[str, Any]:
    tokens: Dict[str, Any] = {}
    token_indexes: Dict[str, int] = {}

    current_token_name = None
    for model_element in model:
        token_name, token_value = next(iter(model_element.items()))

        # Adjust the current token index according to how many
        # consecutive elements of the same type have we parsed
        token_indexes.setdefault(token_name, -1)
        if current_token_name != token_name:
            token_indexes[token_name] += 1

        token_name = f'{token_name}|{token_indexes[token_name]}'

        if token_name in tokens:
            if isinstance(tokens[token_name], list):
                tokens[token_name].append(token_value)
            else:
                tokens[token_name] = [tokens[token_name], token_value]
        else:
            tokens[token_name] = token_value

    return tokens


def _structure_model(model: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any]

    if isinstance(model, dict):
        if len(model) == 1:
            # Single key node
            key, value = next(iter(model.items()))

            if isinstance(value, list):
                if len(value) == 1:
                    # Single value list
                    result = {key: _structure_model(value[0])}
                else:
                    # Multiple values list
                    result = {key: list(map(_structure_model, value))}
            else:
                # Can happen?
                raise NotImplementedError()

        elif is_positional_node(model):
            result = {'Token': model}
        else:
            result = dict(zip(model, map(_structure_model, model.values())))
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def _structure_keys(model: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(model, dict):
        result: Dict[str, Any] = {}
        for key, val in model.items():
            if isinstance(val, dict):
                if key == 'Token' or key.startswith('Token|'):
                    result[key] = val
                else:
                    result[key] = _parse_rule([_structure_keys(val)])
            elif isinstance(val, list):
                result[key] = _parse_rule(list(map(_structure_keys, val)))
            else:
                # Can happen?
                raise NotImplementedError()
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def from_parse_tree(parse_tree: Dict[str, Any]) -> Dict[str, Any]:
    model = parse_tree
    model = _structure_model(model)
    model = _structure_keys(model)

    return model
