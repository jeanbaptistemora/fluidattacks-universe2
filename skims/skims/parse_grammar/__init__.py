# Standard library
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
from utils.logs import (
    log,
)
from utils.system import (
    read,
)

# Constants
AST: str = get_artifact('static/ast/build/install/ast/bin/ast')


@cache_decorator()
async def parse(
    grammar: Union[
        Literal['Java9'],
    ],
    *,
    content: bytes,
    path: str,
) -> Dict[str, Any]:
    code, out_bytes, err_bytes = await read(AST, grammar, stdin_bytes=content)

    try:
        if err_bytes:
            err: str = err_bytes.decode('utf-8')
            await log('debug', 'Parse[%s]: %s, %s', grammar, path, err)
            raise IOError('AST Parser found syntax errors')

        if code != 0:
            raise IOError('AST Parser return non-zero exit code')

        if out_bytes:
            out: str = out_bytes.decode('utf-8')
            data: Dict[str, Any] = await in_process(json.loads, out)
            return data

        raise IOError('No stdout in process')
    except (IOError, json.JSONDecodeError) as exc:
        await log('error', 'Parsing[%s]: %s, %s', grammar, path, exc)
        return {}
