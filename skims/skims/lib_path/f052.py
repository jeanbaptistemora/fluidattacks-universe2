from aioextensions import (
    in_process,
)
from lib_path.common import (
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVA_PROPERTIES,
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
    SINGLE_QUOTED_STRING,
)
from model import (
    core_model,
)
from parse_java_properties import (
    load as load_java_properties,
)
from pyparsing import (
    Keyword,
    MatchFirst,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
    Tuple,
)
from utils.crypto import (
    is_iana_cipher_suite_vulnerable,
    is_open_ssl_cipher_suite_vulnerable,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)


def _java_insecure_pass(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    framework = "org.springframework.security"
    grammar = MatchFirst(
        [
            Keyword(f"{framework}.authentication.encoding.ShaPasswordEncoder"),
            Keyword(f"{framework}.authentication.encoding.Md5PasswordEncoder"),
            Keyword(f"{framework}.crypto.password.LdapShaPasswordEncoder"),
            Keyword(f"{framework}.crypto.password.Md4PasswordEncoder"),
            Keyword(
                f"{framework}.crypto.password.MessageDigestPasswordEncoder"
            ),
            Keyword(f"{framework}.crypto.password.NoOpPasswordEncoder"),
            Keyword(f"{framework}.crypto.password.StandardPasswordEncoder"),
            Keyword(f"{framework}.crypto.scrypt.SCryptPasswordEncoder"),
        ]
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"310", "327"},
        description=t(
            key="src.lib_path.f052.insecure_pass.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_insecure_pass(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_insecure_pass,
        content=content,
        path=path,
    )


def _java_properties_missing_ssl(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    missing_ssl_key: str = "ibm.mq.use_ssl"
    missing_ssl_values: Set[str] = {"false"}

    def _iterate_vulnerabilities() -> Iterator[Tuple[int, int]]:
        for line_no, (key, val) in load_java_properties(content).items():
            if key == missing_ssl_key and val in missing_ssl_values:
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"310", "327"},
        description=t(
            key="src.lib_path.f052.java_properties_missing_ssl",
            path=path,
        ),
        finding=core_model.FindingEnum.F052,
        iterator=_iterate_vulnerabilities(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_properties_missing_ssl(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_properties_missing_ssl,
        content=content,
        path=path,
    )


def _java_properties_weak_cipher_suite(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    weak_cipher_suite: str = "ibm.mq.cipher.suite"

    def _iterate_vulnerabilities() -> Iterator[Tuple[int, int]]:
        for line_no, (key, val) in load_java_properties(content).items():
            if key == weak_cipher_suite and (
                is_iana_cipher_suite_vulnerable(val)
                or is_open_ssl_cipher_suite_vulnerable(val)
            ):
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"310", "327"},
        description=t(
            key="src.lib_path.f052.java_properties_weak_cipher_suite",
            path=path,
        ),
        finding=core_model.FindingEnum.F052,
        iterator=_iterate_vulnerabilities(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_properties_weak_cipher_suite(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_properties_weak_cipher_suite,
        content=content,
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

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(
            java_insecure_pass(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(
            java_properties_missing_ssl(
                content=await content_generator(),
                path=path,
            )
        )
        coroutines.append(
            java_properties_weak_cipher_suite(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
