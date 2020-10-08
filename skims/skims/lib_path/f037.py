# Standar library
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Tuple,
)

# Third party library
from aioextensions import (
    in_process,
    resolve,
)

# Local library
from lib_path.common import (
    blocking_get_vulnerabilities_from_iterator,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from utils.graph import (
    yield_dicts,
)
from parse_babel import (
    parse as parse_babel,
)
from zone import (
    t,
)


def _yield_console_logs(model: Any) -> Iterator[Any]:
    functions = (
        'log',
        'warn',
        'error',
    )
    for node in yield_dicts(model):
        if (node.get('type') == 'CallExpression'
                and node['callee']['object']['name'] == 'console'
                and node['callee']['property']['name'] in functions):
            yield node


def _yield_var_usage(var_name: str, model: Any) -> Iterator[Any]:
    for node in yield_dicts(model):
        if node.get('type') == 'Identifier' and node.get('name') == var_name:
            yield node


def _javascript_use_console_log(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> Tuple[Vulnerability, ...]:
    def iterator() -> Iterator[Tuple[int, int]]:
        for node in yield_dicts(model):
            # interface CatchClause <: Node {
            #   #type: "CatchClause";
            #   param?: Pattern;
            #   body: BlockStatement;
            # }
            if node.get('type') == 'CatchClause':
                if not node.get('param'):
                    # If the exception is not caught in a variable, there
                    # is no way it will be displayed in a console.log
                    # catch {
                    #     console.log();
                    # }
                    continue
                exception_name = node['param']['name']

                for console in _yield_console_logs(node):
                    for arg in console.get('arguments'):
                        # The exception should not be used as an argument to
                        # the console.log
                        # catch (err) {
                        #     console.log(err);
                        # }
                        if tuple(
                                _yield_var_usage(
                                    var_name=exception_name,
                                    model=arg,
                                )):
                            yield (
                                console['loc']['start']['line'],
                                console['loc']['start']['column'],
                            )

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        description=t(
            key='src.lib_path.f037.javascript_use_console_log',
            path=path,
        ),
        finding=FindingEnum.F037,
        iterator=iterator(),
        path=path,
    )


@cache_decorator()
@SHIELD
async def javascript_use_console_log(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_use_console_log,
        content=content,
        model=await parse_babel(
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_use_console_log(
            content=await content_generator(),
            path=path,
        ))
    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
