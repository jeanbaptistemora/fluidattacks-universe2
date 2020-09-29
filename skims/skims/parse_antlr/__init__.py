# Standard library
import contextlib
import json
from typing import (
    Any,
    Dict,
    Union,
    Literal,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from state.cache import (
    cache_decorator,
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
from utils.system import (
    read,
)

# Constants
ANTLR_PARSER: str = get_artifact(
    'static/parsers/antlr/build/install/parse/bin/parse',
)


@cache_decorator()
async def parse(
    grammar: Union[
        Literal['Java9'],
    ],
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
    grammar: Union[
        Literal['Java9'],
    ],
    *,
    content: bytes,
    memory: int,
    path: str,
) -> Dict[str, Any]:
    code, out_bytes, err_bytes = await read(
        ANTLR_PARSER,
        grammar,
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
        await log_exception('error', exc, grammar=grammar, path=path)
        return {}
