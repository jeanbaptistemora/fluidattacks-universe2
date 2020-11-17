# Standard library
from typing import (
    Any,
    Dict,
    List,
)


def _parse_rule(model: List[Dict[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    token_index = 0

    for model_element in model:
        token_name, token_value = next(iter(model_element.items()))

        if token_name == 'Token':
            token_name = f'Token[{token_index}]'
            token_index += 1

        if token_name in result:
            if isinstance(result[token_name], list):
                result[token_name].append(token_value)
            else:
                result[token_name] = [result[token_name], token_value]
        else:
            result[token_name] = token_value

    return result


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

        elif len(model) == 4:
            # Token node
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
                if key == 'Token':
                    result[key] = val
                else:
                    result[key] = _structure_keys(val)
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
