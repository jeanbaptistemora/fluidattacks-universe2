# Standard library
import asyncio
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
from utils.ctx import (
    get_artifact,
)
from utils.logs import (
    log,
)
from utils.system import (
    call,
)

# Constants
AST: str = get_artifact('static/ast/build/install/ast/bin/ast')


async def parse(
    grammar: Union[
        Literal['Java9'],
    ],
    path: str,
) -> Dict[str, Any]:
    process: asyncio.subprocess.Process = await call(AST, grammar, path)

    out_bytes, err_bytes = await process.communicate()

    try:
        if err_bytes:
            err: str = err_bytes.decode('utf-8')
            await log('debug', 'Parse[%s]: %s, %s', grammar, path, err)
            raise IOError('AST Parser found syntax errors')

        if process.returncode != 0:
            raise IOError('AST Parser return non-zero exit code')

        if out_bytes:
            out: str = out_bytes.decode('utf-8')
            data: Dict[str, Any] = await in_process(json.loads, out)
            return data

        raise IOError('No stdout in process')
    except (IOError, json.JSONDecodeError) as exc:
        await log('error', 'Parsing[%s]: %s, %s', grammar, path, exc)
        return {}
