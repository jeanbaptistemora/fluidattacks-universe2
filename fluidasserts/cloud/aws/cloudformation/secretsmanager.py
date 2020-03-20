"""AWS CloudFormation checks for ``SecretsManager``."""

# Standard library
import contextlib
from typing import List, Optional

# Local imports
from fluidasserts import SAST, HIGH
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    CloudFormationInvalidTypeError,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if

# ASCII Constants
NUMERICS: set = set('01234567890')
LOWERCASE: set = set('abcdefghijklmnopqrstuvwxyz')
UPPERCASE: set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
PUNCTUATION: set = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')


def _insecure_generate_secret_string_get_reasons(
        exclude_lower, exclude_upper, exclude_numbers,
        exclude_punctuation, exclude_chars,
        require_each_include_type, password_length, min_length):
    """Helper to append vulnerabilities based on the parameters provided."""
    reasons: List[str] = []

    if exclude_lower:
        reasons.append('Secret must include lowercase characters')

    if exclude_upper:
        reasons.append('Secret must include uppercase characters')

    if exclude_numbers:
        reasons.append('Secret must include numeric characters')

    if exclude_punctuation:
        reasons.append('Using ExcludePunctuation is too agressive'
                       '; use ExcludeCharacters instead')

    for charset_name, charset in (('numeric', NUMERICS),
                                  ('lowercase', LOWERCASE),
                                  ('uppercase', UPPERCASE),
                                  ('punctuation', PUNCTUATION)):
        # Do not allow to entirely exclude one type of chars
        if all(c in exclude_chars for c in charset):
            reasons.append(f'You are excluding the entire {charset_name}'
                           f' charset with ExcludeCharacters')

    if not require_each_include_type:
        reasons.append('RequireEachIncludedType must be "true"')

    if password_length < min_length:
        reasons.append(f'PasswordLength must be >= than {min_length}')

    return reasons


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def insecure_generate_secret_string(path: str,
                                    exclude: Optional[List[str]] = None,
                                    min_length: int = 14) -> tuple:
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
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::SecretsManager::Secret',
            ],
            exclude=exclude):
        res_props_gss = res_props.get('GenerateSecretString')
        if not res_props_gss:
            continue

        exclude_chars: str = res_props_gss.get('ExcludeCharacters', '')
        password_length: str = res_props_gss.get('PasswordLength', 32)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            exclude_lower: str = helper.to_boolean(
                res_props_gss.get('ExcludeLowercase', False))
            exclude_upper: str = helper.to_boolean(
                res_props_gss.get('ExcludeUppercase', False))
            exclude_numbers: str = helper.to_boolean(
                res_props_gss.get('ExcludeNumbers', False))
            exclude_punctuation: str = helper.to_boolean(
                res_props_gss.get('ExcludePunctuation', False))
            require_each_include_type: str = helper.to_boolean(
                res_props_gss.get('RequireEachIncludedType', True))

        reasons: List[str] = _insecure_generate_secret_string_get_reasons(
            exclude_lower=exclude_lower,
            exclude_upper=exclude_upper,
            exclude_numbers=exclude_numbers,
            exclude_punctuation=exclude_punctuation,
            exclude_chars=exclude_chars,
            require_each_include_type=require_each_include_type,
            password_length=password_length,
            min_length=min_length)

        if reasons:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::SecretsManager::Secret',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason)
                for reason in reasons)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='GenerateSecretString is miss-configured',
        msg_closed='GenerateSecretString is properly configured')
