# Standar library
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
)
from contextlib import (
    suppress,
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
    EXTENSIONS_JAVA,
    SHIELD,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Grammar,
    Vulnerability,
)
from utils.graph import (
    yield_dicts,
    yield_nodes,
)
from parse_babel import (
    parse as parse_babel,
)
from parse_antlr import (
    parse as parse_antlr,
)
from zone import (
    t,
)


def _yield_javascript_console_logs(model: Any) -> Iterator[Any]:
    functions = (
        'log',
        'warn',
        'error',
    )
    for node in yield_dicts(model):
        with suppress(KeyError):
            if (node.get('type') == 'CallExpression'
                    and node['callee']['object']['name'] == 'console'
                    and node['callee']['property']['name'] in functions):
                yield node


def _yield_javascript_var_usage(
        var_name: str, model: Any) -> Iterator[Dict[str, Union[str, int]]]:
    for node in yield_dicts(model):
        with suppress(KeyError):
            if node['type'] == 'Identifier' and node['name'] == var_name:
                yield node


def _yield_java_var_usage(
        model: Any, *identifiers: str) -> Iterator[Any]:
    for var_name in identifiers:
        for node in yield_nodes(
                value=model,
                key_predicates=('Identifier'.__eq__, ),
        ):
            if node['text'] == var_name:
                yield node


def _is_java_method_call(node: Any, *members: str) -> bool:
    """Validate if a node is the call of a function"""
    return len(tuple(_yield_java_var_usage(
        node,
        *members,
    ))) == len(members)


def _is_java_logs(model: Any, logger_identifier: str) -> bool:
    log_methods = (
        'info',
        'error',
        'warn',
        'trace',
    )
    return any(
        tuple(
            _is_java_method_call(model, logger_identifier, x)
            for x in log_methods))


def _yield_java_loggers(model: Any) -> Iterator[Any]:
    logger_patterns = (
        ('LogManager', 'getLogger'),
        ('LoggerFactory', 'getLogger'),
        ('Logger', 'getLogger'),
    )
    for invocation in yield_nodes(
            value=model,
            key_predicates=('FieldDeclaration'.__eq__, ),
            pre_extraction=(),
            post_extraction=(),
    ):
        if any((_is_java_method_call(invocation, *pattern)
                for pattern in logger_patterns)):
            yield tuple(
                yield_nodes(
                    value=model,
                    key_predicates=('VariableDeclaratorId'.__eq__, ),
                ))[0]


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
            if node.get('type', None) == 'CatchClause':
                if not node.get('param', None):
                    # If the exception is not caught in a variable, there
                    # is no way it will be displayed in a console.log
                    # catch {
                    #     console.log();
                    # }
                    continue
                exception_name = node['param']['name']

                for console in _yield_javascript_console_logs(node):
                    for arg in console.get('arguments', list()):
                        # The exception should not be used as an argument to
                        # the console.log
                        # catch (err) {
                        #     console.log(err);
                        # }
                        if tuple(
                                _yield_javascript_var_usage(
                                    var_name=exception_name,
                                    model=arg,
                                )):
                            yield (
                                console['loc']['start']['line'],
                                console['loc']['start']['column'],
                            )

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'200', '209'},
        description=t(
            key='src.lib_path.f037.javascript_use_console_log',
            path=path,
        ),
        finding=FindingEnum.F037,
        iterator=iterator(),
        path=path,
    )


def _java_logging_exceptions(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> Tuple[Vulnerability, ...]:
    def iterator() -> Iterator[Tuple[int, int]]:
        loggers = tuple(_yield_java_loggers(model))

        for node in yield_nodes(
                value=model,
                key_predicates=('CatchClause'.__eq__, ),
                pre_extraction=(),
                post_extraction=(),
        ):
            exc_identifier = tuple(item for item in yield_nodes(
                value=node,
                value_extraction='.'.join((
                    '[2]',
                    'CatchFormalParameter[1]',
                    'VariableDeclaratorId[0]',
                    'Identifier[0]',
                )),
                pre_extraction=(),
                post_extraction=(),
            ))[0]

            for call in yield_nodes(
                    value=node[4]['Block'],
                    key_predicates=('MethodInvocation'.__eq__, ),
                    pre_extraction=(),
                    post_extraction=(),
            ):
                if _is_java_method_call(call, exc_identifier['text'],
                                        'printStackTrace'):
                    # verify if use
                    #  catch (IndexException e) {
                    #   e.printStackTrace();
                    #  }
                    yield (call[2]['Identifier'][0]['l'],
                           call[2]['Identifier'][0]['c'])
                elif _is_java_method_call(
                        call,
                        'System',
                        'out',
                        'println',
                ):
                    # validates that the exception is not used as a parameter
                    # of System.out.println
                    # catch (IndexException e) {
                    #     System.out.println(e);
                    # }
                    for var in _yield_java_var_usage(
                            call[4]['ArgumentList'],
                            exc_identifier['text'],
                    ):
                        yield (var['l'], var['c'])
                elif loggers and any(
                        _is_java_logs(call, x['text']) for x in loggers):
                    # validate that the most common loggers are not used with
                    # the exception
                    # catch (IndexException e) {
                    #   logger.info(e);
                    # }
                    arguments = tuple(
                        yield_nodes(
                            value=call,
                            key_predicates=('ArgumentList'.__eq__, ),
                            pre_extraction=(),
                            post_extraction=(),
                        ))[0]
                    for var in _yield_java_var_usage(
                            arguments,
                            exc_identifier['text'],
                    ):
                        yield (var['l'], var['c'])

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'200', '209'},
        description=t(
            key='src.lib_path.f037.java_logging_exceptions',
            path=path,
        ),
        finding=FindingEnum.F037,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_logging_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_logging_exceptions,
        content=content,
        model=await parse_antlr(
            Grammar.JAVA9,
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


@CACHE_ETERNALLY
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
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_logging_exceptions(
            content=await content_generator(),
            path=path,
        ))
    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
