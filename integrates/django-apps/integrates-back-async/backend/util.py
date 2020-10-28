# -*- coding: utf-8 -*-
""" FluidIntegrates auxiliar functions. """

import collections
from datetime import datetime, timedelta, date
import binascii
import functools
import logging
import re
import secrets
import json
from typing import (
    Any,
    cast,
    Dict,
    Iterator,
    List,
    Union,
)
import httpx

from aioextensions import (
    collect,
    in_thread,
    schedule,
)
from asgiref.sync import async_to_sync
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from cryptography.exceptions import InvalidKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from django.core.cache import cache
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from django.http import JsonResponse
from graphql.language.ast import (
    BooleanValueNode,
    FieldNode,
    NameNode,
    ObjectFieldNode,
    ObjectValueNode,
    SelectionSetNode,
    StringValueNode,
    VariableNode
)
from jose import jwt, JWTError
from magic import Magic

from backend.dal import session as session_dal
from backend.dal.helpers.redis import (
    AREDIS_CLIENT,
)
from backend.exceptions import (
    ConcurrentSession,
    ExpiredToken,
    InvalidAuthorization,
    InvalidFileType
)
from backend.typing import (
    Finding as FindingType,
    User as UserType,
    Project as ProjectType
)
from backend.utils import (
    apm,
    datetime as datetime_utils,
    function,
    encodings,
    decodings
)

from backend_new import settings

from fluidintegrates.settings import (
    LOGGING,
    NOEXTRA
)
from __init__ import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
    FORCES_TRIGGER_URL,
    FORCES_TRIGGER_REF,
    FORCES_TRIGGER_TOKEN,
    FI_JWT_ENCRYPTION_KEY
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger('transactional')
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization
MAX_API_AGE_WEEKS = 26  # max exp time of access token 6 months


def response(data: object, message: str, error: bool) -> JsonResponse:
    """ Create an object to send generic answers """
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return JsonResponse(response_data)


def ord_asc_by_criticality(
        data: List[Dict[str, FindingType]]) -> List[Dict[str, FindingType]]:
    """ Sort the findings by criticality """
    for i in range(0, len(data) - 1):
        for j in range(i + 1, len(data)):
            firstc = float(cast(float, data[i]["severityCvss"]))
            seconc = float(cast(float, data[j]["severityCvss"]))
            if firstc < seconc:
                aux = data[i]
                data[i] = data[j]
                data[j] = aux
    return data


def assert_file_mime(filename: str, allowed_mimes: List[str]) -> bool:
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    return mime_type in allowed_mimes


def get_uploaded_file_mime(file_instance: str) -> str:
    mime = Magic(mime=True)
    mime_type = ''
    if isinstance(file_instance, TemporaryUploadedFile):
        mime_type = mime.from_file(file_instance.temporary_file_path())
    elif isinstance(file_instance, InMemoryUploadedFile):
        mime_type = mime.from_buffer(file_instance.file.getvalue())
    else:
        raise InvalidFileType(
            'Provided file is not a valid django upload file. '
            'Use util.assert_file_mime instead.'
        )
    return mime_type


def assert_uploaded_file_mime(
        file_instance: str,
        allowed_mimes: List[str]) -> bool:
    mime_type = get_uploaded_file_mime(file_instance)
    return mime_type in allowed_mimes


def has_release(finding: Dict[str, str]) -> bool:
    return "releaseDate" in finding


def get_last_vuln(finding: Dict[str, str]) -> date:
    """Gets last release of a finding"""
    finding_last_vuln_date = datetime_utils.get_from_str(
        finding["releaseDate"].split(" ")[0],
        date_format='%Y-%m-%d'
    ).date()
    return finding_last_vuln_date


def validate_release_date(finding: Dict[str, str]) -> bool:
    """Validate if a finding has a valid relese date."""
    if has_release(finding):
        last_vuln = get_last_vuln(finding)
        today_day = datetime_utils.get_now().date()
        result = last_vuln <= today_day
    else:
        result = False
    return result


def cloudwatch_log_sync(request, msg: str) -> None:
    try:
        user_data = async_to_sync(get_jwt_content)(request)
        info = [str(user_data['user_email'])]
    except (ExpiredToken, InvalidAuthorization):
        info = ['unauthenticated user']

    for parameter in ['project', 'findingid']:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    LOGGER_TRANSACTIONAL.info(':'.join(info), **NOEXTRA)


def cloudwatch_log(request, msg: str) -> None:
    schedule(cloudwatch_log_async(request, msg))


async def cloudwatch_log_async(request, msg: str) -> None:
    user_data = await get_jwt_content(request)
    info = [str(user_data['user_email'])]
    for parameter in ['project', 'findingid']:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    schedule(
        in_thread(LOGGER_TRANSACTIONAL.info, ':'.join(info), **NOEXTRA))


def encrypt_jwt_payload(payload: dict) -> dict:
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    claims = JWE(
        algs=[
            'A256GCM',
            'A256GCMKW',
        ],
        plaintext=serialized_payload.encode('utf-8'),
        protected={
            'alg': 'A256GCMKW',
            'enc': 'A256GCM',
        },
        recipient=key,
    ).serialize()
    return decodings.jwt_payload_decode(claims)


def decrypt_jwt_payload(payload: dict) -> dict:
    if 'ciphertext' not in payload:
        return payload
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    result = JWE()
    result.deserialize(serialized_payload.encode('utf-8'))
    result.decrypt(key)
    return decodings.jwt_payload_decode(result.payload.decode('utf-8'))


async def get_jwt_content(context) -> Dict[str, str]:
    context_store_key = function.get_id(get_jwt_content)

    # Within the context of one request we only need to process it once
    if context_store_key in context.store:
        return context.store[context_store_key]

    try:
        cookies = context.COOKIES \
            if hasattr(context, 'COOKIES') \
            else context['request'].scope.get('cookies', {})
        cookie_token = cookies.get(settings.JWT_COOKIE_NAME)
        header_token = (
            context.META.get('HTTP_AUTHORIZATION')
            if hasattr(context, 'META')
            else dict(context['request'].scope['headers']).get(
                'Authorization', ''
            )
        )
        token = header_token.split()[1] if header_token else cookie_token
        if not token:
            raise InvalidAuthorization()

        payload = jwt.get_unverified_claims(token)
        payload = decrypt_jwt_payload(payload)
        if is_api_token(payload):
            content = jwt.decode(
                token=token,
                key=settings.JWT_SECRET_API,
                algorithms='HS512'
            )
            content = decrypt_jwt_payload(content)
        else:
            content = jwt.decode(
                token=token,
                key=settings.JWT_SECRET,
                algorithms='HS512'
            )
            content = decrypt_jwt_payload(content)
            jti = content.get('jti')
            if (content.get('sub') == 'django_session' and
                    not await token_exists(f'fi_jwt:{jti}')):
                # Session expired (user logged out)
                raise ExpiredToken()

    except jwt.ExpiredSignatureError:
        # Session expired
        raise InvalidAuthorization()
    except (AttributeError, IndexError) as ex:
        LOGGER.exception(ex, extra={'extra': context})
        raise InvalidAuthorization()
    except jwt.JWTClaimsError as ex:
        LOGGER.info('Security: Invalid token claims', **NOEXTRA)
        LOGGER.warning(ex, extra={'extra': context})
        raise InvalidAuthorization()
    except JWTError as ex:
        LOGGER.info('Security: Invalid token', **NOEXTRA)
        LOGGER.warning(ex, extra={'extra': context})
        raise InvalidAuthorization()
    else:
        context.store[context_store_key] = content
        return content


async def create_confirm_access_token(
    email: str,
    group: str,
    responsibility: str
) -> str:
    token_lifetime = timedelta(weeks=1)

    urltoken = secrets.token_urlsafe(64)

    token = dict(
        user_email=email,
        responsibility=responsibility,
        group=group,
        is_used=False,
    )

    await save_token(
        f'fi_urltoken:{urltoken}',
        json.dumps(token),
        int(token_lifetime.total_seconds())
    )

    return urltoken


def iterate_s3_keys(client, bucket: str, prefix: str) -> Iterator[str]:
    yield from (
        content['Key']
        for response in client.get_paginator('list_objects_v2').paginate(
            Bucket=bucket,
            PaginationConfig={
                'PageSize': 1000,
            },
            Prefix=prefix,
        )
        for content in response.get('Contents', [])
    )


def replace_all(text: str, dic: Dict[str, str]) -> str:
    for i, j in list(dic.items()):
        text = text.replace(i, j)
    return text


def list_to_dict(keys: List[object], values: List[object]) -> \
        Dict[object, object]:
    """ Merge two lists into a {key: value} dictionary """

    dct: Dict[object, object] = collections.OrderedDict()
    index = 0

    if len(keys) < len(values):
        diff = len(values) - len(keys)
        for i in range(diff):
            del i
            keys.append("")
    elif len(keys) > len(values):
        diff = len(keys) - len(values)
        for i in range(diff):
            del i
            values.append("")
    else:
        # Each key has a value associated, so there's no need to empty-fill
        pass

    for item in values:
        if keys[index] == "":
            dct[index] = item
        else:
            dct[keys[index]] = item
        index += 1

    return dct


def camelcase_to_snakecase(str_value: str) -> str:
    """Convert a camelcase string to snackecase."""
    my_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str_value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', my_str).lower()


def snakecase_to_camelcase(str_value: str) -> str:
    """Convert a snackecase string to camelcase."""
    return re.sub('_.', lambda x: x.group()[1].upper(), str_value)


async def invalidate_cache(*keys_pattern: str) -> int:
    """Remove keys from cache that matches a given pattern.

    Return the total number of entries deleted.

    This is a very expensive operation so do not use directly.
    """
    entries_deleted: int = sum(await collect(
        in_thread(cache.delete_pattern, f'*{key_pattern.lower()}*')
        for key_pattern in keys_pattern
    ))

    return entries_deleted


def queue_cache_invalidation(*keys_pattern: str) -> None:
    schedule(invalidate_cache(*keys_pattern))


def format_cache_keys_pattern(attrs_to_clean: Dict[str, str]) -> List[str]:
    return [
        f'{attribute}*{identifier}'
        for attribute, identifier in attrs_to_clean.items()
    ]


def format_comment_date(date_string: str) -> str:
    comment_date = datetime_utils.get_from_str(date_string)
    formatted_date = datetime_utils.get_as_str(
        comment_date,
        date_format='%Y/%m/%d %H:%M:%S'
    )

    return formatted_date


def calculate_datediff_since(start_date: datetime) -> timedelta:
    final_date = (datetime_utils.get_now().date() - start_date.date())

    return abs(final_date)


def is_valid_expiration_time(expiration_time: float) -> bool:
    """Verify that expiration time is minor than six months"""
    exp = datetime.utcfromtimestamp(expiration_time)
    now = datetime.utcnow()
    return now < exp < (now + timedelta(weeks=MAX_API_AGE_WEEKS))


def calculate_hash_token() -> Dict[str, str]:
    jti_token = secrets.token_bytes(NUMBER_OF_BYTES)
    salt = secrets.token_bytes(NUMBER_OF_BYTES)
    backend = default_backend()
    jti_hashed = Scrypt(
        salt=salt,
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend
    ).derive(jti_token)

    return {
        'jti_hashed': binascii.hexlify(jti_hashed).decode(),
        'jti': binascii.hexlify(jti_token).decode(),
        'salt': binascii.hexlify(salt).decode()
    }


def verificate_hash_token(access_token: Dict[str, str], jti_token: str) -> \
        bool:
    resp = False
    backend = default_backend()
    token_hashed = Scrypt(
        salt=binascii.unhexlify(access_token['salt']),
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend
    )
    try:
        token_hashed.verify(
            binascii.unhexlify(jti_token),
            binascii.unhexlify(access_token['jti']))
        resp = True
    except InvalidKey as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))

    return resp


def is_api_token(user_data: UserType) -> bool:
    return user_data.get('sub') == (
        'api_token'
        if 'sub' in user_data
        else 'jti' in user_data
    )


def is_valid_format(date_str: str) -> bool:
    try:
        datetime_utils.get_from_str(date_str)
        resp = True
    except ValueError:
        resp = False

    return resp


def forces_trigger_deployment(project_name: str) -> bool:
    def callback(client: httpx.AsyncClient, _):
        schedule(client.aclose())

    success = False

    # cast it to string, just in case
    project_name = str(project_name).lower()

    parameters = {
        'ref': FORCES_TRIGGER_REF,
        'token': FORCES_TRIGGER_TOKEN,
        'variables[subs]': project_name,
    }

    try:
        if project_name not in FI_TEST_PROJECTS.split(','):
            client = httpx.AsyncClient()
            req_coro = client.post(
                url=FORCES_TRIGGER_URL,
                files={
                    param: (None, value)
                    for param, value in parameters.items()
                }
            )
            task = schedule(req_coro)
            task.add_done_callback(functools.partial(callback, client))

    except httpx.HTTPError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    else:
        success = True
    return success


def update_treatment_values(updated_values: Dict[str, str]) -> Dict[str, str]:
    if updated_values['treatment'] == 'NEW':
        updated_values['acceptance_date'] = ''
    elif updated_values['treatment'] == 'ACCEPTED_UNDEFINED':
        updated_values['acceptance_status'] = 'SUBMITTED'
        days = [
            datetime_utils.get_now_plus_delta(days=x + 1)
            for x in range(5)
        ]
        weekend_days = sum(1 for day in days if day.weekday() >= 5)
        updated_values['acceptance_date'] = datetime_utils.get_as_str(
            datetime_utils.get_now_plus_delta(days=5 + weekend_days)
        )
    return updated_values


def get_requested_fields(field_name: str, selection_set: SelectionSetNode) -> \
        List[FieldNode]:
    """Get requested fields from selections."""
    try:
        field_set = list(
            filter(
                lambda sel: sel.name.value == field_name,
                selection_set.selections
            )
        )
        selections = field_set[0].selection_set.selections
    except IndexError:
        selections = []
    return selections


@apm.trace()
def get_field_parameters(
        field: FieldNode,
        variable_values: Dict[str, Any] = None) -> Dict[str, Any]:
    """Get a dict of parameters for field."""
    if not hasattr(field, 'arguments'):
        return {}
    if not field.arguments:
        return {}

    parameters = {}
    variable_values = variable_values or {}

    for args in field.arguments:
        arg_name = camelcase_to_snakecase(args.name.value)

        if isinstance(args.value, VariableNode):
            parameters[arg_name] = variable_values.get(args.value.name.value)
        elif isinstance(args.value, NameNode):
            parameters[arg_name] = args.value.value
        elif isinstance(args.value, ObjectValueNode):
            parameters[arg_name] = args.value.fields
        else:
            parameters[arg_name] = args.value.value

    return parameters


def is_skippable(info, field: FieldNode) -> Any:
    """Check if field is need to be skipped."""
    if not hasattr(field, 'directives'):
        return False
    if not field.directives:
        return False
    include_dir = list(
        filter(lambda dire: dire.name.value == 'include', field.directives)
    )
    if not include_dir:
        return False
    arg_val = include_dir[0].arguments[0].value
    if isinstance(arg_val, NameNode):
        var_name = include_dir[0].arguments[0].value.name.value
        return not info.variable_values[var_name]
    if isinstance(arg_val, BooleanValueNode):
        var_name = include_dir[0].arguments[0].value.value
        return not var_name
    var_name = include_dir[0].arguments[0].value.name.value
    return not info.variable_values[var_name]


def camel_case_list_dict(elements: List[Dict]) -> List[Dict]:
    """Convert a the keys of a list of dicts to camelcase."""
    return [
        {
            snakecase_to_camelcase(k): element[k]
            for k in element
        }
        for element in elements
    ]


def dict_to_object_field_node(input_dict: Dict[str, Any]) -> \
        List[Union[None, ObjectFieldNode]]:
    """Convert a dict into a list of ObjectFieldNode objects."""
    if not input_dict:
        return []
    result = []
    for key in input_dict:
        ofn = ObjectFieldNode(
            name=NameNode(value=key),
            value=StringValueNode(value=str(input_dict[key]))
        )
        result.append(ofn)
    return result


async def get_filtered_elements(elements, filters) -> List[ProjectType]:
    """Return filtered findings accorging to filters."""

    async def satisfies_filter(element) -> bool:
        hits = 0
        for attribute, value in filters.items():
            result = element.get(camelcase_to_snakecase(attribute))
            if str(result) == str(value):
                hits += 1
        return hits == len(filters)

    conditions = await collect(map(satisfies_filter, elements))

    return [
        element
        for element, condition in zip(elements, conditions)
        if condition
    ]


async def check_concurrent_sessions(email: str, session_key: str):
    """
    This method checks if current user
    already has an active session and if so, removes it
    """
    previous_session_key = await session_dal.get_previous_session(
        email, session_key
    )
    if previous_session_key:
        await session_dal.invalidate_session(previous_session_key)
        raise ConcurrentSession()


async def save_token(key: str, token: str, time: int):
    await session_dal.add_element(key, token, time)


async def remove_token(key: str):
    await session_dal.remove_element(key)


async def get_token(key: str) -> str:
    return await AREDIS_CLIENT.get(key)


async def token_exists(key: str) -> bool:
    return await session_dal.element_exists(key)


async def get_ttl_token(key: str) -> int:
    return await AREDIS_CLIENT.ttl(key)
