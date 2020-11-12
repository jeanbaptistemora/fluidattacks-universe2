# Standard library
from collections import (
    defaultdict,
)
import contextlib
import json
from typing import (
    Any,
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.ctx import (
    get_artifact,
)
from utils.hardware import (
    get_memory_semaphore,
    iterate_host_memory_levels,
)
from utils.logs import (
    log_exception,
)
from utils.model import (
    Grammar,
)
from utils.system import (
    read,
)

# Constants
PARSER: str = get_artifact(
    'static/parsers/antlr/build/install/parse/bin/parse',
)


@CACHE_ETERNALLY
async def parse(
    grammar: Grammar,
    *,
    content: bytes,
    path: str,
) -> Dict[str, Any]:
    for memory in iterate_host_memory_levels():
        async with get_memory_semaphore().acquire_many(memory):
            with contextlib.suppress(MemoryError):
                return await _parse(
                    content=content,
                    grammar=grammar,
                    memory=memory,
                    path=path,
                )

    return {}


async def _parse(
    grammar: Grammar,
    *,
    content: bytes,
    memory: int,
    path: str,
) -> Dict[str, Any]:
    code, out_bytes, err_bytes = await read(
        PARSER,
        grammar.value,
        env=dict(
            # Limit heap size
            JAVA_OPTS=f'-Xmx{memory}g',
        ),
        stdin_bytes=content,
    )

    try:
        if err_bytes:
            err: str = err_bytes.decode('utf-8')

            if 'Not enough memory' in err:
                raise MemoryError(err)

            raise IOError(err)

        if code != 0:
            raise IOError('ANTLR Parser returned a non-zero exit code')

        if out_bytes:
            out: str = out_bytes.decode('utf-8')
            data: Dict[str, Any] = await in_process(json.loads, out)
            return data

        raise IOError('No stdout in process')
    except (IOError, json.JSONDecodeError) as exc:
        await log_exception('error', exc, grammar=grammar.value, path=path)
        return {}


def parse_rule(
    model: List[Dict[str, Any]],
    values: Dict[str, Any],
) -> Dict[str, Any]:
    token_index = 0

    for model_element in model:
        if all(key in model_element for key in ('c', 'l', 'text', 'type')):
            model_element = {f'__token__.{token_index}': model_element}
            token_index += 1

        token_name, token_value = next(iter(model_element.items()))

        if token_name not in values:
            raise ValueError(f'Expected values to contain: {token_name}')

        if isinstance(values[token_name], list):
            values[token_name].append(token_value)
        else:
            values[token_name] = token_value

    return values


def parse_rule2(model: List[Dict[str, Any]]) -> Dict[str, Any]:
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


def structure_model(model: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any]

    if isinstance(model, dict):
        if len(model) == 1:
            # Single key node
            key, value = next(iter(model.items()))

            if isinstance(value, list):
                if len(value) == 1:
                    # Single value list
                    result = {key: format_model(value[0])}
                else:
                    # Multiple values list
                    result = {key: list(map(format_model, value))}
            else:
                # Can happen?
                raise NotImplementedError()

        elif len(model) == 4:
            # Token node
            result = {'Token': model}
        else:
            result = dict(zip(model.keys(), map(format_model, model.values())))
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def structure_keys(model: Dict[str, Any]) -> defaultdict:
    if isinstance(model, dict):
        result: defaultdict = defaultdict(None)
        for key, val in model.items():
            if isinstance(val, dict):
                result[key] = val
            elif isinstance(val, list):
                result[key] = parse_rule2(val)
            else:
                # Can happen?
                raise NotImplementedError()
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def format_model(model: Dict[str, Any]) -> defaultdict:
    return structure_keys(structure_model(model))
