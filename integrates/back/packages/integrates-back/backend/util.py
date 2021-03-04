# -*- coding: utf-8 -*-
""" Integrates auxiliar functions. """

import collections
import os
from datetime import datetime, timedelta
import binascii
import logging
import re
import secrets
from typing import (
    Any,
    cast,
    Dict,
    Iterator,
    List,
    Union
)
import magic
from aioextensions import (
    collect,
    in_thread,
    schedule,
)
from cryptography.exceptions import InvalidKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
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
from jwcrypto.jwe import InvalidJWEData
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile

from back import settings
from backend.dal import (
    session as session_dal,
)
from backend.dal.helpers.redis import (
    redis_get_entity_attr,
)
from backend.exceptions import (
    ExpiredToken,
    InvalidAuthorization,
    InvalidSource,
)
from backend.model import redis_model
from backend.typing import (
    Finding as FindingType,
    User as UserType,
    Project as ProjectType
)
from backend.utils import token as token_helper
from newutils import (
    apm,
    datetime as datetime_utils,
    function,
)
from __init__ import (
    FI_ENVIRONMENT,
)

logging.config.dictConfig(settings.LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger('transactional')
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization
MAX_API_AGE_WEEKS = 26  # max exp time of access token 6 months


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
    mime_type = magic.from_file(filename, mime=True)
    return mime_type in allowed_mimes


async def get_uploaded_file_mime(file_instance: UploadFile) -> str:
    mime_type: str = magic.from_buffer(await file_instance.read(), mime=True)
    await file_instance.seek(0)
    return mime_type


async def assert_uploaded_file_mime(
        file_instance: UploadFile,
        allowed_mimes: List[str]) -> bool:
    mime_type = await get_uploaded_file_mime(file_instance)
    return mime_type in allowed_mimes


def cloudwatch_log(request, msg: str) -> None:
    schedule(cloudwatch_log_async(request, msg))


async def cloudwatch_log_async(request, msg: str) -> None:
    user_data = await get_jwt_content(request)
    info = [str(user_data['user_email'])]
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    schedule(
        in_thread(
            LOGGER_TRANSACTIONAL.info, ':'.join(info),
            **settings.NOEXTRA
        )
    )


async def get_jwt_content(context) -> Dict[str, str]:  # noqa: MC0001
    context_store_key = function.get_id(get_jwt_content)

    if isinstance(context, dict):
        context = context.get('request', {})
    store = get_request_store(context)

    # Within the context of one request we only need to process it once
    if context_store_key in store:
        return store[context_store_key]

    try:
        cookies = context.cookies
        cookie_token = cookies.get(settings.JWT_COOKIE_NAME)

        header_token = context.headers.get('Authorization')

        token = header_token.split()[1] if header_token else cookie_token

        if context.session.get('username'):
            await session_dal.check_jwt_token_validity(context)

        if not token:
            raise InvalidAuthorization()

        if token_helper.jwt_has_api_token(token):
            content = token_helper.decode_jwt(token, api=True)
        else:
            content = token_helper.decode_jwt(token)
            if content.get('sub') == 'starlette_session':
                try:
                    await redis_get_entity_attr(
                        entity='session',
                        attr='jti',
                        email=content['user_email']
                    )
                except redis_model.KeyNotFound:
                    # Session expired (user logged out)
                    raise ExpiredToken()

    except jwt.ExpiredSignatureError:
        # Session expired
        raise InvalidAuthorization()
    except (AttributeError, IndexError) as ex:
        LOGGER.exception(ex, extra={'extra': context})
        raise InvalidAuthorization()
    except jwt.JWTClaimsError as ex:
        LOGGER.info('Security: Invalid token claims', **settings.NOEXTRA)
        LOGGER.warning(ex, extra={'extra': context})
        raise InvalidAuthorization()
    except JWTError as ex:
        LOGGER.info('Security: Invalid token', **settings.NOEXTRA)
        LOGGER.warning(ex, extra={'extra': context})
        raise InvalidAuthorization()
    except InvalidJWEData:
        raise InvalidAuthorization()
    else:
        store[context_store_key] = content
        return content


def get_source(context: Any) -> str:
    headers = context.headers
    source = headers.get('x-integrates-source', 'integrates')
    if source not in {'integrates', 'skims'}:
        raise InvalidSource()

    return source


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


async def get_file_size(file_object: UploadFile) -> int:
    file = file_object.file

    # Needed while upstream starlette implements a size method
    # pylint: disable=protected-access
    if file_object._in_memory:
        current_position = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(current_position)
    else:
        current_position = await run_in_threadpool(file.tell)
        await run_in_threadpool(file.seek, 0, os.SEEK_END)
        size = await run_in_threadpool(file.tell)
        await run_in_threadpool(file.seek, current_position)

    return size


def get_request_store(context) -> collections.defaultdict:
    """ Returns customized store attribute of a Django/Starlette request"""

    return context.store if hasattr(context, 'store') else context.state.store
