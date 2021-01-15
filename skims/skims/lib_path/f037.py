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
)

# Local library
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
)
from model import (
    core_model,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.graph import (
    yield_dicts,
    yield_nodes,
)
from parse_babel import (
    parse as parse_babel,
)
from parse_antlr.parse import (
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


def _javascript_use_console_log(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> core_model.Vulnerabilities:
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

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'200', '209'},
        description=t(
            key='src.lib_path.f037.javascript_use_console_log',
            path=path,
        ),
        finding=core_model.FindingEnum.F037,
        iterator=iterator(),
        path=path,
    )


def _java_logging_exceptions(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> core_model.Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:

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

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'200', '209'},
        description=t(
            key='src.lib_path.f037.java_print_stack_traces',
            path=path,
        ),
        finding=core_model.FindingEnum.F037,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_logging_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_logging_exceptions,
        content=content,
        model=await parse_antlr(
            core_model.Grammar.JAVA9,
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def javascript_use_console_log(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _javascript_use_console_log,
        content=content,
        model=await parse_babel(
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_use_console_log(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
