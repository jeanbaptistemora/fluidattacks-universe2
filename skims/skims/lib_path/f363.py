from aioextensions import (
    in_process,
)
from aws.model import (
    AWSSecretsManagerSecret,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_secret_manager_secrets,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F363 = core_model.FindingEnum.F363
_FINDING_F363_CWE = _FINDING_F363.value.cwe


# pylint: disable=too-many-arguments
def get_insecure_generate_secret_vulns(
    gen_secret_str_node: Node,
    exclude_lower: bool,
    exclude_upper: bool,
    exclude_numbers: bool,
    exclude_punctuation: bool,
    exclude_chars: str,
    require_each_include_type: bool,
    password_length: int,
) -> Iterator[Node]:
    # ASCII Constants
    numerics: set = set("01234567890")
    lowercase: set = set("abcdefghijklmnopqrstuvwxyz")
    uppercase: set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    punctuation: set = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    min_length = 14

    if exclude_lower:
        yield gen_secret_str_node.inner["ExcludeLowercase"]

    if exclude_upper:
        yield gen_secret_str_node.inner["ExcludeUppercase"]

    if exclude_numbers:
        yield gen_secret_str_node.inner["ExcludeNumbers"]

    if exclude_punctuation:
        yield gen_secret_str_node.inner["ExcludePunctuation"]

    for charset in (
        numerics,
        lowercase,
        uppercase,
        punctuation,
    ):
        # Do not allow to entirely exclude one type of chars
        if all(char in exclude_chars for char in charset):
            yield gen_secret_str_node.inner["ExcludeCharacters"]

    if not require_each_include_type:
        yield gen_secret_str_node.inner["RequireEachIncludedType"]

    if password_length < min_length:
        yield gen_secret_str_node.inner["PasswordLength"]


def _cfn_insecure_generate_secret_string_iterate_vulnerabilities(
    secrets_iterator: Iterator[Union[AWSSecretsManagerSecret, Node]],
) -> Iterator[Union[AWSSecretsManagerSecret, Node]]:
    for secret in secrets_iterator:
        gen_secret_str = get_node_by_keys(secret, ["GenerateSecretString"])
        if isinstance(gen_secret_str, Node):
            exclude_chars = gen_secret_str.raw.get("ExcludeCharacters", "")
            password_length = gen_secret_str.raw.get("PasswordLength", 32)
            exclude_lower = gen_secret_str.raw.get("ExcludeLowercase", False)
            exclude_upper = gen_secret_str.raw.get("ExcludeUppercase", False)
            exclude_numbers = gen_secret_str.raw.get("ExcludeNumbers", False)
            exclude_punctuation = gen_secret_str.raw.get(
                "ExcludePunctuation", False
            )
            require_each_include_type = gen_secret_str.raw.get(
                "RequireEachIncludedType", False
            )

            yield from get_insecure_generate_secret_vulns(
                gen_secret_str,
                exclude_lower,
                exclude_upper,
                exclude_numbers,
                exclude_punctuation,
                exclude_chars,
                require_each_include_type,
                password_length,
            )


def _cfn_insecure_generate_secret_string(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F363_CWE},
        description_key="src.lib_path.f363.insecure_generate_secret_string",
        finding=_FINDING_F363,
        iterator=get_cloud_iterator(
            _cfn_insecure_generate_secret_string_iterate_vulnerabilities(
                secrets_iterator=iter_secret_manager_secrets(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_insecure_generate_secret_string(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_insecure_generate_secret_string,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_insecure_generate_secret_string(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
