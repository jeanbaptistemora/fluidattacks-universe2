# -*- coding: utf-8 -*-
""" FluidIntegrates auxiliar functions. """
from __future__ import absolute_import
import collections
from datetime import datetime
import binascii
import hashlib
import logging
import logging.config
import re
import secrets
import pytz
import rollbar

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey
from magic import Magic
from django.conf import settings
from django.http import JsonResponse
from django.core.files.uploadedfile import (
    TemporaryUploadedFile, InMemoryUploadedFile
)
from django.core.cache import cache
from jose import jwt, JWTError
# pylint: disable=E0402
from __init__ import FI_ENVIRONMENT
from .exceptions import InvalidAuthorization


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization


def response(data, message, error):
    """ Create an object to send generic answers """
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return JsonResponse(response_data)


def is_name(name):
    """ Verify that a parameter has the appropriate name format. """
    valid = True
    try:
        if not name or not name.isalnum():
            raise ValueError('')
    except ValueError:
        valid = False
    return valid


def is_numeric(name):
    """ Verify that a parameter has the appropriate number format. """
    valid = True
    try:
        if not name or not name.isdigit():
            raise ValueError('')
    except ValueError:
        valid = False
    return valid


def ord_asc_by_criticidad(data):
    """ Sort the findings by criticality """
    for i in range(0, len(data) - 1):
        for j in range(i + 1, len(data)):
            firstc = float(data[i]["severityCvss"])
            seconc = float(data[j]["severityCvss"])
            if firstc < seconc:
                aux = data[i]
                data[i] = data[j]
                data[j] = aux
    return data


def drive_url_filter(drive):
    """ Gets the ID of an image stored on Google Drive """
    if drive.find("id=") != -1:
        new_url = drive.split("id=")[1]
        if new_url.find("&") != -1:
            return new_url.split("&")[0]
    return drive


def get_evidence_set(finding):
    evidence_set = []
    if "evidence_route_1" in finding and "evidence_description_1" in finding:
        evidence_set.append({
            "id": finding["evidence_route_1"],
            "explanation": finding["evidence_description_1"].capitalize()
        })
    if "evidence_route_2" in finding and "evidence_description_2" in finding:
        evidence_set.append({
            "id": finding["evidence_route_2"],
            "explanation": finding["evidence_description_2"].capitalize()
        })
    if "evidence_route_3" in finding and "evidence_description_3" in finding:
        evidence_set.append({
            "id": finding["evidence_route_3"],
            "explanation": finding["evidence_description_3"].capitalize()
        })
    if "evidence_route_4" in finding and "evidence_description_4" in finding:
        evidence_set.append({
            "id": finding["evidence_route_4"],
            "explanation": finding["evidence_description_4"].capitalize()
        })
    if "evidence_route_5" in finding and "evidence_description_5" in finding:
        evidence_set.append({
            "id": finding["evidence_route_5"],
            "explanation": finding["evidence_description_5"].capitalize()
        })
    return evidence_set


def get_evidence_set_s3(finding, key_list, field_list):
    evidence_set = []
    for k in key_list:
        for i in range(1, 6):
            evidence_route = \
                '{project}/{findingid}/{project}-{findingid}-{fieldid}'.format(
                    project=finding['projectName'].lower(),
                    findingid=finding['id'],
                    fieldid=field_list[i - 1])
            description = 'evidence_description_' + str(i)
            if description in finding and \
                    evidence_route in k:
                evidence_set.append({
                    'id': k,
                    'explanation': finding[description].capitalize()
                })
    return evidence_set


def user_email_filter(emails, actual_user):
    if "@fluidattacks.com" in actual_user:
        final_users = emails
    else:
        final_users = list(filter(lambda email: not(
            email.endswith('@fluidattacks.com')), emails))
    return final_users


def assert_file_mime(filename, allowed_mimes):
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    return mime_type in allowed_mimes


def assert_uploaded_file_mime(file_instance, allowed_mimes):
    mime = Magic(mime=True)
    if isinstance(file_instance, TemporaryUploadedFile):
        mime_type = mime.from_file(file_instance.temporary_file_path())
    elif isinstance(file_instance, InMemoryUploadedFile):
        mime_type = mime.from_buffer(file_instance.file.getvalue())
    else:
        raise Exception('Provided file is not a valid django upload file. \
                            Use util.assert_file_mime instead.')
    return mime_type in allowed_mimes


def has_release(finding):
    return "releaseDate" in finding


def get_last_vuln(finding):
    """Gets last release of a finding"""
    tzn = pytz.timezone(settings.TIME_ZONE)
    finding_last_vuln = datetime.strptime(
        finding["releaseDate"].split(" ")[0],
        '%Y-%m-%d'
    )
    finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
    return finding_last_vuln


def validate_release_date(finding):
    """Validate if a finding has a valid relese date."""
    if has_release(finding):
        last_vuln = get_last_vuln(finding)
        tzn = pytz.timezone(settings.TIME_ZONE)
        today_day = datetime.now(tz=tzn).date()
        result = last_vuln <= today_day
    else:
        result = False
    return result


def validate_future_releases(finding):
    """Validate if a finding has a future release."""
    if has_release(finding):
        last_vuln = get_last_vuln(finding)
        tzn = pytz.timezone(settings.TIME_ZONE)
        today_day = datetime.now(tz=tzn).date()
        result = last_vuln > today_day
    else:
        result = False
    return result


def cloudwatch_log(request, msg):
    user_data = get_jwt_content(request)
    info = [user_data["user_email"], user_data["company"]]
    for parameter in ["project", "findingid"]:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    LOGGER.info(":".join(info))


def get_jwt_content(context):
    try:
        cookie_token = context.COOKIES.get(settings.JWT_COOKIE_NAME)
        header_token = context.META.get('HTTP_AUTHORIZATION')
        token = header_token.split()[1] if header_token else cookie_token
        payload = jwt.get_unverified_claims(token)

        if payload.get('jti'):
            content = jwt.decode(
                token=token, key=settings.JWT_SECRET_API, algorithms='HS512')
        else:
            content = jwt.decode(
                token=token, key=settings.JWT_SECRET, algorithms='HS512')

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


def list_s3_objects(client_s3, bucket_s3, key):
    resp = client_s3.list_objects_v2(
        Bucket=bucket_s3,
        Prefix=key,
    )
    key_list = []
    for obj in resp.get('Contents', []):
        key_list.append(obj['Key'])

    return key_list


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def list_to_dict(keys, values):
    """ Merge two lists into a {key: value} dictionary """

    dct = collections.OrderedDict()
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


def camelcase_to_snakecase(str_value):
    """Convert a camelcase string to snackecase."""
    my_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str_value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', my_str).lower()


def snakecase_to_camelcase(str_value):
    """Convert a snackecase string to camelcase."""
    return re.sub('_.', lambda x: x.group()[1].upper(), str_value)


def invalidate_cache(key_pattern):
    """Remove keys from cache that matches a given pattern."""
    cache.delete_pattern('*' + str(key_pattern).lower() + '*')


def calculate_etag(_, img_file):
    """Calculate Etag for given file."""
    try:
        img_id = img_file.split('.')[0][-4:]
        etag = '{}-{}'.format(img_id,
                              hashlib.md5(open(img_file, 'rb').read()).hexdigest())
        return etag
    except (OSError, AttributeError):
        return None


def is_valid_file_name(name):
    """ Verify that filename has valid characters. """
    is_valid = bool(re.search("^[A-Za-z0-9!_.*'()&$@=;:+,? -]*$", str(name)))
    return is_valid


def format_comment_date(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    date = date.strftime('%Y/%m/%d %H:%M:%S')

    return date


def calculate_datediff_since(start_date):
    tzn = pytz.timezone(settings.TIME_ZONE)
    start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d')
    start_date = start_date.replace(tzinfo=tzn).date()
    final_date = (datetime.now(tz=tzn).date() - start_date)
    return final_date


def calculate_hash_token():
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
        'jti_hashed': binascii.hexlify(jti_hashed),
        'jti': binascii.hexlify(jti_token),
        'salt': binascii.hexlify(salt)
    }


def verificate_hash_token(access_token, jti_token):
    resp = False
    backend = default_backend()
    token_hashed = Scrypt(
        salt=binascii.unhexlify(access_token['access_token']['salt']),
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend
    )
    try:
        token_hashed.verify(
            binascii.unhexlify(jti_token),
            binascii.unhexlify(access_token['access_token']['jti']))
        resp = True
    except InvalidKey:
        rollbar.report_message('Error: Access token does not match', 'error')

    return resp
