from aws.model import (
    AWSSecretsManagerSecret,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_secret_manager_secrets,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


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


def cfn_insecure_generate_secret_string(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f363.insecure_generate_secret_string",
        iterator=get_cloud_iterator(
            _cfn_insecure_generate_secret_string_iterate_vulnerabilities(
                secrets_iterator=iter_secret_manager_secrets(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_INSEC_GEN_SECRET,
    )
