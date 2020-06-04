# -*- coding: utf-8 -*-
""" FluidIntegrates auxiliar functions. """

import asyncio
import collections
from datetime import datetime, timedelta, timezone
import binascii
import functools
import logging
import logging.config
import re
import secrets
from typing import Any, Dict, Iterator, List, Union, cast
import httpx
import pytz
import rollbar


from asgiref.sync import sync_to_async
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey
from graphql.language.ast import (
    BooleanValueNode, NameNode, ObjectFieldNode, ObjectValueNode,
    VariableNode, SelectionSetNode, FieldNode, StringValueNode
)
from magic import Magic
from django.conf import settings
from django.http import JsonResponse
from django.core.files.uploadedfile import (
    TemporaryUploadedFile, InMemoryUploadedFile
)
from django.core.cache import cache
from jose import jwt, JWTError


from backend.dal import session as session_dal
from backend.exceptions import (
    ConcurrentSession, InvalidAuthorization,
    InvalidDate, InvalidDateFormat,
)

from backend.typing import Finding as FindingType, User as UserType
from __init__ import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
    FORCES_TRIGGER_URL,
    FORCES_TRIGGER_REF,
    FORCES_TRIGGER_TOKEN
)

logging.config.dictConfig(settings.LOGGING)  # type: ignore
LOGGER = logging.getLogger(__name__)
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


def get_current_time_minus_delta(*, weeks: int) -> datetime:
    """ Return a customized no-naive date n weeks back to the past """
    now = datetime.utcnow()
    now_minus_delta = now - timedelta(weeks=weeks)
    now_minus_delta = now_minus_delta.replace(tzinfo=timezone.utc)
    return now_minus_delta


def get_current_time_as_iso_str() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def user_email_filter(emails: List[str], actual_user: str) -> List[str]:
    if "@fluidattacks.com" in actual_user:
        final_users = emails
    else:
        final_users = list([email for email in emails if not(
            email.endswith('@fluidattacks.com'))])
    return final_users


def assert_file_mime(filename: str, allowed_mimes: List[str]) -> bool:
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    return mime_type in allowed_mimes


def assert_uploaded_file_mime(file_instance: str, allowed_mimes: List[str]) -> bool:
    mime = Magic(mime=True)
    if isinstance(file_instance, TemporaryUploadedFile):
        mime_type = mime.from_file(file_instance.temporary_file_path())
    elif isinstance(file_instance, InMemoryUploadedFile):
        mime_type = mime.from_buffer(file_instance.file.getvalue())
    else:
        raise Exception('Provided file is not a valid django upload file. \
                            Use util.assert_file_mime instead.')
    return mime_type in allowed_mimes


def has_release(finding: Dict[str, str]) -> bool:
    return "releaseDate" in finding


def get_last_vuln(finding: Dict[str, str]) -> datetime:
    """Gets last release of a finding"""
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    finding_last_vuln = datetime.strptime(
        finding["releaseDate"].split(" ")[0],
        '%Y-%m-%d'
    )
    finding_last_vuln_date = finding_last_vuln.replace(tzinfo=tzn).date()
    return cast(datetime, finding_last_vuln_date)


def validate_release_date(finding: Dict[str, str]) -> bool:
    """Validate if a finding has a valid relese date."""
    if has_release(finding):
        last_vuln = get_last_vuln(finding)
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        today_day = datetime.now(tz=tzn).date()
        result = last_vuln <= today_day
    else:
        result = False
    return result


def cloudwatch_log(request, msg: str) -> None:
    asyncio.create_task(cloudwatch_log_queue(request, msg))


def cloudwatch_log_sync(request, msg: str) -> None:
    user_data = get_jwt_content(request)
    info = [str(user_data["user_email"]), str(user_data["company"])]
    for parameter in ["project", "findingid"]:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    LOGGER.info(":".join(info))


async def cloudwatch_log_queue(request, msg: str) -> None:
    user_data = get_jwt_content(request)
    info = [str(user_data["user_email"]), str(user_data["company"])]
    for parameter in ["project", "findingid"]:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    asyncio.create_task(sync_to_async(LOGGER.info)(":".join(info)))


def get_jwt_content(context) -> Dict[str, str]:
    try:
        cookies = context.COOKIES \
            if hasattr(context, 'COOKIES') \
            else context['request'].scope.get('cookies', {})
        cookie_token = cookies.get(settings.JWT_COOKIE_NAME)  # type: ignore
        header_token = context.META.get('HTTP_AUTHORIZATION') \
            if hasattr(context, 'META') \
            else dict(context['request'].scope['headers']).get('Authorization', '')
        token = header_token.split()[1] if header_token else cookie_token
        payload = jwt.get_unverified_claims(token)

        if payload.get('jti'):
            content = jwt.decode(
                token=token, key=settings.JWT_SECRET_API, algorithms='HS512')  # type: ignore
        else:
            content = jwt.decode(
                token=token, key=settings.JWT_SECRET, algorithms='HS512')  # type: ignore

        return content
    except AttributeError:
        raise InvalidAuthorization()
    except IndexError:
        rollbar.report_message(
            'Error: Malformed auth header', 'error', context)
        raise InvalidAuthorization()
    except JWTError:
        LOGGER.info('Security: Invalid token signature')
        raise InvalidAuthorization()


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


def list_to_dict(keys: List[object], values: List[object]) -> Dict[object, object]:
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


def invalidate_cache(key_pattern: str) -> None:
    """Remove keys from cache that matches a given pattern."""
    cache.delete_pattern('*' + str(key_pattern).lower() + '*')


def is_valid_file_name(name: str) -> bool:
    """ Verify that filename has valid characters. """
    name = str(name)
    name_len = len(name.split('.'))
    if name_len <= 2:
        is_valid = bool(re.search("^[A-Za-z0-9!_.*'()&$@=;:+,? -]*$", str(name)))
    else:
        is_valid = False
    return is_valid


def format_comment_date(date_string: str) -> str:
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    formatted_date = date.strftime('%Y/%m/%d %H:%M:%S')

    return formatted_date


def calculate_datediff_since(start_date: datetime) -> timedelta:
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    start_date = datetime.strptime(str(start_date).split(' ')[0], '%Y-%m-%d')
    start_date = cast(datetime, start_date.replace(tzinfo=tzn).date())
    final_date = (datetime.now(tz=tzn).date() - start_date)
    return final_date


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


def verificate_hash_token(access_token: Dict[str, str], jti_token: str) -> bool:
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
    except InvalidKey:
        rollbar.report_message('Error: Access token does not match', 'error')

    return resp


def is_api_token(user_data: UserType) -> bool:
    is_api = bool(user_data.get('jti'))

    return is_api


def is_valid_format(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        resp = True
    except ValueError:
        resp = False

    return resp


def forces_trigger_deployment(project_name: str) -> bool:
    def callback(client: httpx.AsyncClient, _):
        asyncio.create_task(client.aclose())

    success = False

    # pylint: disable=protected-access
    exceptions = (
        httpx._exceptions.ConnectTimeout,
        httpx._exceptions.ConnectionClosed,
        httpx._exceptions.CookieConflict,
        httpx._exceptions.DecodingError,
        httpx._exceptions.HTTPError,
        httpx._exceptions.InvalidURL,
        httpx._exceptions.NetworkError,
        httpx._exceptions.NotRedirectResponse,
        httpx._exceptions.PoolTimeout,
        httpx._exceptions.ProtocolError,
        httpx._exceptions.ProxyError,
        httpx._exceptions.ReadTimeout,
        httpx._exceptions.RedirectError,
        httpx._exceptions.RequestBodyUnavailable,
        httpx._exceptions.RequestNotRead,
        httpx._exceptions.ResponseClosed,
        httpx._exceptions.ResponseNotRead,
        httpx._exceptions.StreamConsumed,
        httpx._exceptions.StreamError,
        httpx._exceptions.TimeoutException,
        httpx._exceptions.TooManyRedirects,
        httpx._exceptions.WriteTimeout,
    )

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
            task = asyncio.create_task(req_coro)
            task.add_done_callback(functools.partial(callback, client))

    except exceptions:
        rollbar.report_exc_info()
    else:
        success = True
    return success


def update_treatment_values(updated_values: Dict[str, str]) -> Dict[str, str]:
    updated_values['external_bts'] = updated_values.get('bts_url', '')
    date = datetime.now() + timedelta(days=180)
    if updated_values.get('bts_url'):
        del updated_values['bts_url']

    if updated_values['treatment'] == 'NEW':
        updated_values['acceptance_date'] = ''
    if updated_values['treatment'] == 'ACCEPTED':
        if updated_values.get('acceptance_date', '') == '':
            max_date = date.strftime('%Y-%m-%d %H:%M:%S')
            updated_values['acceptance_date'] = max_date
        date_size = updated_values['acceptance_date'].split(' ')
        if len(date_size) == 1:
            updated_values['acceptance_date'] += ' ' + datetime.now().strftime('%H:%M:%S')
        date_value = updated_values['acceptance_date']
        is_valid_date = is_valid_format(date_value)
        if is_valid_date is False:
            raise InvalidDateFormat()
        if updated_values.get('acceptance_date'):
            today_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if str(updated_values.get('acceptance_date', '')) <= today_date \
               or str(updated_values.get('acceptance_date', '')) > \
               date.strftime('%Y-%m-%d %H:%M:%S'):
                raise InvalidDate()
    if updated_values['treatment'] == 'ACCEPTED_UNDEFINED':
        updated_values['acceptation_approval'] = 'SUBMITTED'
        today = datetime.now()
        days = [
            today + timedelta(x + 1) for x in range((today + timedelta(days=5) - today).days)]
        weekend_days = sum(1 for day in days if day.weekday() >= 5)
        updated_values['acceptance_date'] = (
            datetime.now() + timedelta(days=5 + weekend_days)).strftime('%Y-%m-%d %H:%M:%S')
    return updated_values


def get_requested_fields(field_name: str, selection_set: SelectionSetNode) -> List[FieldNode]:
    """Get requested fields from selections."""
    try:
        field_set = list(
            filter(lambda sel: sel.name.value == field_name,
                   selection_set.selections)
        )
        selections = field_set[0].selection_set.selections
    except IndexError:
        selections = []
    return selections


def get_field_parameters(field: FieldNode,
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


def dict_to_object_field_node(input_dict: dict) -> List[Union[None, ObjectFieldNode]]:
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


async def get_filtered_elements(elements, filters):
    """Return filtered findings accorging to filters."""
    # This should be called with all() in the future, but there's a known bug
    # of Python that currently prevents it: https://bugs.python.org/issue39562
    filtered = []
    if filters:
        for element in elements:
            hit_counter = 0
            len_filters = len(filters)
            for filt in filters:
                filt_key = camelcase_to_snakecase(filt.name.value)
                coro_result = await element[filt_key]
                if str(coro_result) == str(filt.value.value):
                    hit_counter += 1
            if hit_counter == len_filters:
                filtered.append(element)
    else:
        filtered = elements
    return filtered


def check_concurrent_sessions(email: str, session_key: str):
    """ This method checks if current user already has an active session and if so, removes it"""
    previous_session_key = session_dal.get_previous_session(email, session_key)
    if previous_session_key:
        session_dal.invalidate_session(previous_session_key)
        raise ConcurrentSession()
