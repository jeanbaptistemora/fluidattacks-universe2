# Standard library
import contextlib
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from pyparsing import (
    Keyword,
    MatchFirst,
    Optional,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVA_PROPERTIES,
    NUMBER,
    SHIELD,
    SINGLE_QUOTED_STRING,
    str_to_number,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    blocking_to_snippet,
)
from zone import (
    t,
)


def _csharp_insecure_cipher(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = (
        MatchFirst([
            Keyword('DES'),
            Keyword('DESCryptoServiceProvider'),
            Keyword('TripleDES'),
            Keyword('TripleDESCng'),
            Keyword('TripleDESCryptoServiceProvider'),
            Keyword('RC2'),
            Keyword('RC2CryptoServiceProvider'),
        ]) +
        Optional(
            '.' +
            MatchFirst([
                Keyword('Create'),
                Keyword('CreateDecryptor'),
                Keyword('CreateEncryptor'),
            ])
        ) +
        '('
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_cipher.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def csharp_insecure_cipher(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_insecure_cipher,
        content=content,
        path=path,
    )


def _csharp_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        Keyword('HMACMD5'),
        Keyword('HMACRIPEMD160'),
        Keyword('HMACSHA1'),
        Keyword('MACTripleDES'),
        Keyword('MD5'),
        Keyword('MD5Cng'),
        Keyword('MD5CryptoServiceProvider'),
        Keyword('MD5Managed'),
        Keyword('RIPEMD160'),
        Keyword('RIPEMD160Managed'),
        Keyword('SHA1'),
        Keyword('SHA1Cng'),
        Keyword('SHA1CryptoServiceProvider'),
        Keyword('SHA1Managed'),
    ]) + Optional('.' + Keyword('Create')) + '('
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_hash.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def csharp_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_insecure_hash,
        content=content,
        path=path,
    )


def _vuln_cipher_get_instance(transformation: str) -> bool:
    alg, mode, pad, *_ = (transformation + '///').split('/', 3)

    return any((
        alg == 'aes' and not mode,
        alg == 'aes' and mode == 'ecb',
        alg == 'aes' and mode == 'cbc' and pad and pad != 'nopadding',
        alg == 'blowfish',
        alg == 'des',
        alg == 'desede',
        alg == 'rc2',
        alg == 'rc4',
        alg == 'rsa' and 'oaep' not in pad,
    ))


def _java_insecure_cipher(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        (
            Keyword('Cipher') + '.' +
            Keyword('getInstance') + '(' +
            DOUBLE_QUOTED_STRING.copy().addCondition(
                lambda tokens: _vuln_cipher_get_instance(tokens[0].lower())
            )
        ),
        (
            Keyword('SSLContext') + '.' +
            Keyword('getInstance') + '(' +
            DOUBLE_QUOTED_STRING.copy().addCondition(
                lambda tokens: tokens[0].lower() not in {
                    "tls",
                    "tlsv1.2",
                    "tlsv1.3",
                    "dtls",
                    "dtlsv1.2",
                    "dtlsv1.3",
                }
            )
        ),
    ])
    grammar.ignore(C_STYLE_COMMENT)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_cipher.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_insecure_cipher(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_cipher,
        content=content,
        path=path,
    )


def _java_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        (
            Keyword('MessageDigest') + '.' +
            Keyword('getInstance') + '(' +
            DOUBLE_QUOTED_STRING.copy().addCondition(
                lambda tokens: tokens[0].lower() in {
                    'md2',
                    'md4',
                    'md5',
                    'sha1',
                    'sha-1',
                }
            )
        ),
        (
            Keyword('DigestUtils') + '.' +
            MatchFirst([
                Keyword('getMd2Digest'),
                Keyword('getMd5Digest'),
                Keyword('getShaDigest'),
                Keyword('getSha1Digest'),
                Keyword('md2'),
                Keyword('md2Hex'),
                Keyword('md5'),
                Keyword('md5Hex'),
                Keyword('sha'),
                Keyword('shaHex'),
                Keyword('sha1'),
                Keyword('sha1Hex'),
            ]) + '('
        ),
        (
            Keyword('Hashing') + '.' +
            MatchFirst([
                Keyword('adler32'),
                Keyword('crc32'),
                Keyword('crc32c'),
                Keyword('goodFastHash'),
                Keyword('hmacMd5'),
                Keyword('hmacSha1'),
                Keyword('md5'),
                Keyword('sha1'),
            ]) + '('
        ),
        Keyword('MGF1ParameterSpec') + '.' + Keyword('SHA1'),
    ])
    grammar.ignore(C_STYLE_COMMENT)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_hash.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_hash,
        content=content,
        path=path,
    )


def _java_insecure_key(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        (
            Keyword('RSAKeyGenParameterSpec') + '(' +
            NUMBER.copy().addCondition(
                lambda tokens: str_to_number(tokens[0]) < 2048
            )
        ),
        (
            Keyword('ECGenParameterSpec') + '(' +
            DOUBLE_QUOTED_STRING.copy().addCondition(
                # openssl ecparam -list_curves
                lambda tokens: tokens[0].lower() in {
                    'secp112r1',
                    'secp112r2',
                    'secp128r1',
                    'secp128r2',
                    'secp160k1',
                    'secp160r1',
                    'secp160r2',
                    'secp192k1',
                    'prime192v1',
                    'prime192v2',
                    'prime192v3',
                    'sect113r1',
                    'sect113r2',
                    'sect131r1',
                    'sect131r2',
                    'sect163k1',
                    'sect163r1',
                    'sect163r2',
                    'sect193r1',
                    'sect193r2',
                    'c2pnb163v1',
                    'c2pnb163v2',
                    'c2pnb163v3',
                    'c2pnb176v1',
                    'c2tnb191v1',
                    'c2tnb191v2',
                    'c2tnb191v3',
                    'c2pnb208w1',
                    'wap-wsg-idm-ecid-wtls1',
                    'wap-wsg-idm-ecid-wtls3',
                    'wap-wsg-idm-ecid-wtls4',
                    'wap-wsg-idm-ecid-wtls5',
                    'wap-wsg-idm-ecid-wtls6',
                    'wap-wsg-idm-ecid-wtls7',
                    'wap-wsg-idm-ecid-wtls8',
                    'wap-wsg-idm-ecid-wtls9',
                    'wap-wsg-idm-ecid-wtls10',
                    'wap-wsg-idm-ecid-wtls11',
                    'oakley-ec2n-3',
                    'oakley-ec2n-4',
                    'brainpoolp160r1',
                    'brainpoolp160t1',
                    'brainpoolp192r1',
                    'brainpoolp192t1',
                }
            )
        ),
    ])
    grammar.ignore(C_STYLE_COMMENT)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_key.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_insecure_key(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_key,
        content=content,
        path=path,
    )


def _java_insecure_pass(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    framework = 'org.springframework.security'
    grammar = MatchFirst([
        Keyword(f'{framework}.authentication.encoding.ShaPasswordEncoder'),
        Keyword(f'{framework}.authentication.encoding.Md5PasswordEncoder'),
        Keyword(f'{framework}.crypto.password.LdapShaPasswordEncoder'),
        Keyword(f'{framework}.crypto.password.Md4PasswordEncoder'),
        Keyword(f'{framework}.crypto.password.MessageDigestPasswordEncoder'),
        Keyword(f'{framework}.crypto.password.NoOpPasswordEncoder'),
        Keyword(f'{framework}.crypto.password.StandardPasswordEncoder'),
        Keyword(f'{framework}.crypto.scrypt.SCryptPasswordEncoder'),
    ])
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.insecure_pass.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_insecure_pass(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_pass,
        content=content,
        path=path,
    )


def _java_properties_missing_ssl(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    missing_ssl_key: str = 'ibm.mq.use_ssl'
    missing_ssl_values: Set[str] = {'false'}

    def _iterate_vulnerabilities() -> Iterator[Tuple[int, int]]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            # Strip comments
            if '#' in line:
                line = line.split('#', maxsplit=1)[0]

            # Split in key and value
            with contextlib.suppress(ValueError):
                key, val = line.strip().split('=', maxsplit=1)
                key, val = key.strip(), val.strip()
                if key == missing_ssl_key and val in missing_ssl_values:
                    yield line_no, 0

    return tuple(
        Vulnerability(
            finding=FindingEnum.F052,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_no}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f052.java_properties_missing_ssl',
                    path=path,
                ),
                snippet=blocking_to_snippet(
                    column=column,
                    content=content,
                    line=line_no,
                )
            )
        )
        for line_no, column in _iterate_vulnerabilities()
    )


@cache_decorator()
@SHIELD
async def java_properties_missing_ssl(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_properties_missing_ssl,
        content=content,
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_insecure_cipher(
            content=await content_generator(),
            path=path,
        ))
        coroutines.append(csharp_insecure_hash(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_insecure_cipher(
            content=await content_generator(),
            path=path,
        ))
        coroutines.append(java_insecure_hash(
            content=await content_generator(),
            path=path,
        ))
        coroutines.append(java_insecure_key(
            content=await content_generator(),
            path=path,
        ))
        coroutines.append(java_insecure_pass(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(java_properties_missing_ssl(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
