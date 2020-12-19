# Standard library
import contextlib
import json
from typing import (
    Any,
    Dict,
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
    log,
)
from utils.model import (
    Grammar,
)
from utils.system import (
    read,
)

# Constants
VERSION: int = 0
PARSER: str = get_artifact(
    'static/parsers/antlr/build/install/parse/bin/parse',
)


async def parse(
    grammar: Grammar,
    *,
    content: bytes,
    path: str,
) -> Dict[str, Any]:
    result = await _parse(
        grammar,
        content=content,
        _=VERSION,
    )

    if result == {}:
        await log('error', 'Unable to parse %s: %s', grammar.value, path)

    return result


@CACHE_ETERNALLY
async def _parse(
    grammar: Grammar,
    *,
    content: bytes,
    _: int,
) -> Dict[str, Any]:
    for memory in iterate_host_memory_levels():
        async with get_memory_semaphore().acquire_many(memory):
            with contextlib.suppress(MemoryError):
                return await __parse(
                    content=content,
                    grammar=grammar,
                    memory=memory,
                )

    return {}


async def __parse(
    grammar: Grammar,
    *,
    content: bytes,
    memory: int,
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
    except (IOError, json.JSONDecodeError):
        return {}
