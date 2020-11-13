# Standard library
import contextlib
from uuid import (
    uuid4 as uuid,
)
import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

# Third party libraries
import networkx as nx

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
            data: Dict[str, Any] = json.loads(out)
            return data

        raise IOError('No stdout in process')
    except (IOError, json.JSONDecodeError) as exc:
        await log_exception('error', exc, grammar=grammar.value, path=path)
        return {}


def parse_rule(model: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                    result = {key: structure_model(value[0])}
                else:
                    # Multiple values list
                    result = {key: list(map(structure_model, value))}
            else:
                # Can happen?
                raise NotImplementedError()

        elif len(model) == 4:
            # Token node
            result = {'Token': model}
        else:
            result = dict(zip(model, map(structure_model, model.values())))
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def structure_keys(model: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(model, dict):
        result: Dict[str, Any] = {}
        for key, val in model.items():
            if isinstance(val, dict):
                if key == 'Token':
                    result[key] = val
                else:
                    result[key] = structure_keys(val)
            elif isinstance(val, list):
                result[key] = parse_rule(list(map(structure_keys, val)))
            else:
                # Can happen?
                raise NotImplementedError()
    else:
        # Can happen?
        raise NotImplementedError()

    return result


def format_model(model: Dict[str, Any]) -> Dict[str, Any]:
    return structure_keys(structure_model(model))


def _node_has_position_metadata(node: Dict[str, Any]) -> bool:
    return set(node.keys()) == {'c', 'l', 'text', 'type'}


def _create_leaf(
    graph: nx.OrderedDiGraph,
    index: int,
    key: Optional[str],
    parent: Optional[str],
    value: Any,
) -> nx.OrderedDiGraph:
    node_id: str = f'{key}.{uuid().hex}' if key else uuid().hex

    # Add a new node and link it to the parent
    graph.add_node(node_id)
    if parent:
        graph.add_edge(parent, node_id, index=index)

    if isinstance(value, dict):
        if _node_has_position_metadata(value):
            for value_key, value_value in value.items():
                graph.nodes[node_id][value_key] = value_value
        else:
            graph = model_to_graph(
                model=value,
                _graph=graph,
                _parent=node_id,
            )
    elif isinstance(value, list):
        graph = model_to_graph(
            model=value,
            _graph=graph,
            _parent=node_id,
        )
    else:
        # May happen?
        raise NotImplementedError()

    return graph


def model_to_graph(
    model: Any,
    _graph: Optional[nx.OrderedDiGraph] = None,
    _parent: Optional[str] = None,
) -> nx.OrderedDiGraph:
    # Handle first level of recurssion, where _graph is None
    graph = nx.OrderedDiGraph() if _graph is None else _graph

    if isinstance(model, dict):
        for index, (key, value) in enumerate(model.items()):
            _create_leaf(
                graph=graph,
                index=index,
                key=key,
                parent=_parent,
                value=value,
            )
    elif isinstance(model, list):
        for index, value in enumerate(model):
            _create_leaf(
                graph=graph,
                index=index,
                key=None,
                parent=_parent,
                value=value,
            )
    else:
        # May happen?
        raise NotImplementedError()

    return graph
