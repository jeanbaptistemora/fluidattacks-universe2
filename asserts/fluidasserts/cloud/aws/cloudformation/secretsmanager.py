"""AWS CloudFormation checks for ``SecretsManager``."""


import contextlib
from fluidasserts import (
    HIGH,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_ref_inverse,
    get_ref_nodes,
    get_resources,
    get_templates,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.helper.aws import (
    CloudFormationInvalidTypeError,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from networkx import (
    DiGraph,
)
from typing import (
    List,
    Optional,
)

# ASCII Constants
NUMERICS: set = set("01234567890")
LOWERCASE: set = set("abcdefghijklmnopqrstuvwxyz")
UPPERCASE: set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
PUNCTUATION: set = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


def _insecure_generate_secret_string_get_reasons(
    exclude_lower,
    exclude_upper,
    exclude_numbers,
    exclude_punctuation,
    exclude_chars,
    require_each_include_type,
    password_length,
    min_length,
):
    """Helper to append vulnerabilities based on the parameters provided."""
    reasons: List[str] = []

    if exclude_lower:
        reasons.append("Secret must include lowercase characters")

    if exclude_upper:
        reasons.append("Secret must include uppercase characters")

    if exclude_numbers:
        reasons.append("Secret must include numeric characters")

    if exclude_punctuation:
        reasons.append(
            "Using ExcludePunctuation is too agressive"
            "; use ExcludeCharacters instead"
        )

    for charset_name, charset in (
        ("numeric", NUMERICS),
        ("lowercase", LOWERCASE),
        ("uppercase", UPPERCASE),
        ("punctuation", PUNCTUATION),
    ):
        # Do not allow to entirely exclude one type of chars
        if all(c in exclude_chars for c in charset):
            reasons.append(
                f"You are excluding the entire {charset_name}"
                f" charset with ExcludeCharacters"
            )

    if not require_each_include_type:
        reasons.append('RequireEachIncludedType must be "true"')

    if password_length < min_length:
        reasons.append(f"PasswordLength must be >= than {min_length}")

    return reasons


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def insecure_generate_secret_string(
    path: str, exclude: Optional[List[str]] = None, min_length: int = 14
) -> tuple:
    """
    Check if any ``AWS::SecretsManager::Secret` is weak configured.

    ``AWS::SecretsManager::Secret`` entity creates a secret and stores it the
    Secrets Manager.

    You can either set the ``SecretString`` attribute, or
    ``GenerateSecretString``.
    In the later case, you are in charge of picking
    secure values to be used in the secret generation.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :param min_length: Secrets are required to be generated with greater than
        or equal length than this parameter.
    :returns: - ``OPEN`` if **GenerateSecretString** attribute is
                miss-configured which will produce weak secrets.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates = get_templates(graph, path, exclude)
    secrets = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "SecretsManager", "Secret"},
        info=True,
    )
    for secret, resource, template in secrets:
        string = helper.get_index(
            get_resources(graph, secret, "GenerateSecretString"), 0
        )
        if not string:
            continue
        exclude_chars_node: str = helper.get_index(
            get_ref_nodes(
                graph,
                get_resources(graph, string, "ExcludeCharacters")[0],
                lambda x: isinstance(x, str),
            ),
            0,
        )
        exclude_chars = (
            graph.nodes[exclude_chars_node]["value"]
            if exclude_chars_node
            else ""
        )
        password_length_node: str = helper.get_index(
            get_ref_nodes(
                graph,
                get_resources(graph, string, "PasswordLength")[0],
                lambda x: isinstance(x, (float, int)),
            ),
            0,
        )
        password_length = (
            graph.nodes[password_length_node]["value"]
            if password_length_node
            else 32
        )
        with contextlib.suppress(CloudFormationInvalidTypeError):
            exclude_lower_node: str = helper.get_index(
                get_ref_nodes(
                    graph,
                    get_resources(graph, string, "ExcludeLowercase")[0],
                    helper.is_boolean,
                ),
                0,
            )
            exclude_lower: bool = (
                helper.to_boolean(graph.nodes[exclude_lower_node]["value"])
                if exclude_lower_node
                else False
            )

            exclude_upper_node: str = helper.get_index(
                get_ref_nodes(
                    graph,
                    get_resources(graph, string, "ExcludeUppercase")[0],
                    helper.is_boolean,
                ),
                0,
            )
            exclude_upper = (
                helper.to_boolean(graph.nodes[exclude_upper_node]["value"])
                if exclude_upper_node
                else False
            )

            exclude_numbers_node: str = helper.get_index(
                get_ref_nodes(
                    graph,
                    get_resources(graph, string, "ExcludeNumbers")[0],
                    helper.is_boolean,
                ),
                0,
            )
            exclude_numbers = (
                helper.to_boolean(graph.nodes[exclude_numbers_node]["value"])
                if exclude_numbers_node
                else False
            )

            exclude_punctuation_node: str = helper.get_index(
                get_ref_nodes(
                    graph,
                    get_resources(graph, string, "ExcludePunctuation")[0],
                    helper.is_boolean,
                ),
                0,
            )
            exclude_punctuation = (
                helper.to_boolean(
                    graph.nodes[exclude_punctuation_node]["value"]
                )
                if exclude_punctuation_node
                else False
            )

            require_each_include_type_node: str = helper.get_index(
                get_ref_nodes(
                    graph,
                    get_resources(graph, string, "RequireEachIncludedType")[0],
                    helper.is_boolean,
                ),
                0,
            )
            require_each_include_type = (
                helper.to_boolean(
                    graph.nodes[require_each_include_type_node]["value"]
                )
                if require_each_include_type_node
                else False
            )

        reasons: List[str] = _insecure_generate_secret_string_get_reasons(
            exclude_lower=exclude_lower,
            exclude_upper=exclude_upper,
            exclude_numbers=exclude_numbers,
            exclude_punctuation=exclude_punctuation,
            exclude_chars=exclude_chars,
            require_each_include_type=require_each_include_type,
            password_length=password_length,
            min_length=min_length,
        )

        if reasons:
            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity="AWS::SecretsManager::Secret",
                    identifier=resource["name"],
                    line=graph.nodes[string]["line"],
                    reason=reason,
                )
                for reason in reasons
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="GenerateSecretString is miss-configured",
        msg_closed="GenerateSecretString is properly configured",
    )
