# Standard library
import io
import os
import re
import json
import time
import contextlib
import datetime
import multiprocessing
import traceback
from typing import Any
from itertools import repeat

# Third parties libraries
import boto3
import botocore.exceptions
import pynamodb.models
import pynamodb.attributes
import ruamel.yaml.reader

# Local libraries
from toolbox import logger, utils, api

# False positives
# pylint: disable=not-callable

# We need to have this static reference alive
assert os

# Constants
BUCKET: str = 'break-build-logs'
DEFAULT_COLUMN_VALUE: str = 'unable to retrieve'
DEFAULT_COLUMN_DATE_VALUE: datetime.datetime = \
    utils.rfc3339_str_to_date_obj(
        utils.guess_date_from_str(DEFAULT_COLUMN_VALUE))
DYNAMO_DB_TABLE: str = 'bb_executions'
LOGS_DATE_FMT = r'%Y%m%d%H%M%S'
REGEX_LOGS_NAME = re.compile(
    r'^(?P<subscription>[a-z]+)'
    r'/(?P<execution_id>[0-9a-f]+)'
    r'/(?P<date>[0-9]+)'
    r'/(?P<kind>[a-z]+)'
    r'/(?P<name>[a-z\-]+)\.yaml$')
REGEX_BUILD_ENV = re.compile(r'^BUILD_ENV=(.*)$', flags=re.MULTILINE)
REGEX_BUILD_TRIGGER_SOURCE = \
    re.compile(r'^BUILD_TRIGGER_SOURCE=(.*)$', flags=re.MULTILINE)
REGEX_EXIT_CODE = re.compile(r'^EXIT_CODE=(.*)$', flags=re.MULTILINE)
REGEX_FA_STRICT = re.compile(r'^FA_STRICT=(.*)$', flags=re.MULTILINE)
REGEX_GIT_BRANCH = re.compile(r'^GIT_BRANCH=(.*)$', flags=re.MULTILINE)
REGEX_GIT_COMMIT = re.compile(r'^GIT_COMMIT=(.*)$', flags=re.MULTILINE)
REGEX_GIT_COMMIT_AUTHOR = \
    re.compile(r'^GIT_COMMIT_AUTHOR=(.*)$', flags=re.MULTILINE)
REGEX_GIT_COMMIT_AUTHORED_DATE = \
    re.compile(r'^GIT_COMMIT_AUTHORED_DATE=(.*)$', flags=re.MULTILINE)
REGEX_GIT_ORIGIN = re.compile(r'^GIT_ORIGIN=(.*)$', flags=re.MULTILINE)
REGEXES_GIT_REPO_FROM_ORIGIN = [
    # https://xxxx.visualstudio.com/xxx/_git/repo_name
    re.compile(r'^.*visualstudio.com/.*/_git/(.*)$'),
    # https://xxx@gitlab.com/xxx/repo_name.git
    re.compile(r'^.*gitlab.com/.*/(.*).git$'),
]


def retrieve_from_s3(s3_client, log_s3_key) -> str:
    """Return as a safe utf8 string the provided s3 object."""
    logger.info(f'Downloading s3://{log_s3_key}')

    # In-memory buffer to store the download
    bytes_io = io.BytesIO()

    # Download it
    s3_client.download_fileobj(BUCKET, log_s3_key, bytes_io)

    # Decode and return the contents
    bytes_io.seek(0)
    return bytes_io.read().decode('utf8', errors='replace')


def get_initial_date_to_sync_from() -> datetime.datetime:
    """Return a customized date to start fetching logs."""
    now = datetime.datetime.utcnow()
    now_minus_delta = now - datetime.timedelta(days=1)
    now_minus_delta = now_minus_delta.replace(tzinfo=datetime.timezone.utc)
    return now_minus_delta


class Execution(pynamodb.models.Model):
    """A PyDynamoDB model to represent a row in the table."""
    class Meta:
        table_name = DYNAMO_DB_TABLE

    subscription = pynamodb.attributes.UnicodeAttribute(hash_key=True)
    execution_id = pynamodb.attributes.UnicodeAttribute(range_key=True)
    date = pynamodb.attributes.UTCDateTimeAttribute()
    kind = pynamodb.attributes.UnicodeAttribute()
    log = pynamodb.attributes.UnicodeAttribute()
    exit_code = pynamodb.attributes.UnicodeAttribute()
    strictness = pynamodb.attributes.UnicodeAttribute()
    build_env = pynamodb.attributes.UnicodeAttribute()
    build_trigger_source = pynamodb.attributes.UnicodeAttribute()
    git_branch = pynamodb.attributes.UnicodeAttribute()
    git_commit = pynamodb.attributes.UnicodeAttribute()
    git_commit_author = pynamodb.attributes.UnicodeAttribute()
    git_commit_authored_date = pynamodb.attributes.UTCDateTimeAttribute()
    git_origin = pynamodb.attributes.UnicodeAttribute()
    git_repo = pynamodb.attributes.UnicodeAttribute()
    vulnerabilities: pynamodb.attributes.MapAttribute = \
        pynamodb.attributes.MapAttribute()
    vulnerabilities_exploits: Any = \
        pynamodb.attributes.ListAttribute()
    vulnerabilities_mocked_exploits: Any = \
        pynamodb.attributes.ListAttribute()
    vulnerabilities_accepted_exploits: Any = \
        pynamodb.attributes.ListAttribute()
    vulnerability_count_exploits: Any = \
        pynamodb.attributes.NumberAttribute()
    vulnerability_count_mocked_exploits: Any = \
        pynamodb.attributes.NumberAttribute()
    vulnerability_count_accepted_exploits: Any = \
        pynamodb.attributes.NumberAttribute()


def get_execution_attr_full(s3_client, s3_prefix):
    full = DEFAULT_COLUMN_VALUE
    with contextlib.suppress(botocore.exceptions.ClientError):
        full = retrieve_from_s3(s3_client, f'{s3_prefix}/full.yaml')
    return full


def get_vulnerabilities_from_log(s3_client, s3_path, git_repo):
    """Return info about a log of exploits."""
    try:
        log_content = retrieve_from_s3(s3_client, s3_path)

        git_repo = '.' if git_repo == DEFAULT_COLUMN_VALUE else git_repo

        data = [
            {
                'kind': str(kind) or DEFAULT_COLUMN_VALUE,
                'who': str(who) or DEFAULT_COLUMN_VALUE,
                'where': str(where) or DEFAULT_COLUMN_VALUE,
            }
            for kind, who, where in api.asserts.iterate_results_from_content(
                log_content, git_repo)
        ]
    except (botocore.exceptions.ClientError,
            ruamel.yaml.reader.ReaderError,
            KeyError):
        return [], 0
    else:
        return data, len(data)


def get_vulnerability_attrs(s3_client, s3_prefix, git_repo) -> dict:
    """Return the vulnerabilities found in the exploit logs."""
    vulns_exploits, len_vulns_exploits = \
        get_vulnerabilities_from_log(
            s3_client, f'{s3_prefix}/exploits.yaml', git_repo)

    vulns_mocked_exploits, len_vulns_mocked_exploits = \
        get_vulnerabilities_from_log(
            s3_client, f'{s3_prefix}/mocked-exploits.yaml', git_repo)

    vulns_accepted_exploits, len_vulns_accepted_exploits = \
        get_vulnerabilities_from_log(
            s3_client, f'{s3_prefix}/accepted-exploits.yaml', git_repo)

    return {
        'exploits': vulns_exploits,
        'mocked_exploits': vulns_mocked_exploits,
        'accepted_exploits': vulns_accepted_exploits,
        'vulnerability_count_exploits': len_vulns_exploits,
        'vulnerability_count_mocked_exploits': len_vulns_mocked_exploits,
        'vulnerability_count_accepted_exploits': len_vulns_accepted_exploits,
    }


def get_metadata_attrs(s3_client, s3_prefix) -> dict:
    """"Return attributes found in the metadata.list file."""
    build_env = DEFAULT_COLUMN_VALUE
    build_trigger_source = DEFAULT_COLUMN_VALUE
    exit_code = DEFAULT_COLUMN_VALUE
    strictness = DEFAULT_COLUMN_VALUE
    git_branch = DEFAULT_COLUMN_VALUE
    git_commit = DEFAULT_COLUMN_VALUE
    git_commit_author = DEFAULT_COLUMN_VALUE
    git_commit_authored_date = DEFAULT_COLUMN_DATE_VALUE
    git_origin = DEFAULT_COLUMN_VALUE
    git_repo = DEFAULT_COLUMN_VALUE

    with contextlib.suppress(botocore.exceptions.ClientError):
        metadata = retrieve_from_s3(s3_client, f'{s3_prefix}/metadata.list')

        # Here is when I want to be in python3.8 (walrus operator) :=
        match = REGEX_BUILD_ENV.search(metadata)
        if match and match.group(1):
            build_env = match.group(1)

        match = REGEX_BUILD_TRIGGER_SOURCE.search(metadata)
        if match and match.group(1):
            build_trigger_source = match.group(1)

        match = REGEX_EXIT_CODE.search(metadata)
        if match and match.group(1):
            exit_code = match.group(1)

        match = REGEX_FA_STRICT.search(metadata)
        if match and match.group(1):
            strictness = 'strict' if match.group(1) == 'true' else 'lax'

        match = REGEX_GIT_BRANCH.search(metadata)
        if match and match.group(1):
            git_branch = match.group(1)

        match = REGEX_GIT_COMMIT.search(metadata)
        if match and match.group(1):
            git_commit = match.group(1)

        match = REGEX_GIT_COMMIT_AUTHOR.search(metadata)
        if match and match.group(1):
            git_commit_author = match.group(1)

        match = REGEX_GIT_COMMIT_AUTHORED_DATE.search(metadata)
        if match and match.group(1):
            git_commit_authored_date = \
                utils.rfc3339_str_to_date_obj(
                    utils.guess_date_from_str(match.group(1)))

        match = REGEX_GIT_ORIGIN.search(metadata)
        if match and match.group(1):
            git_origin = match.group(1)

            for regex in REGEXES_GIT_REPO_FROM_ORIGIN:
                match = regex.match(git_origin)
                if match and match.group(1):
                    git_repo = match.group(1)

    return dict(
        build_env=build_env,
        build_trigger_source=build_trigger_source,
        exit_code=exit_code,
        strictness=strictness,
        git_branch=git_branch,
        git_commit=git_commit,
        git_commit_author=git_commit_author,
        git_commit_authored_date=git_commit_authored_date,
        git_origin=git_origin,
        git_repo=git_repo,
    )


def get_execution_object(s3_client, execution_group_match) -> Execution:
    """Return an execution Object with all columns filled."""
    execution_group_match_json = \
        json.dumps(execution_group_match.groupdict(), indent=2)

    logger.info(f'Processing {execution_group_match_json}')

    subscription = execution_group_match.group('subscription')
    execution_id = execution_group_match.group('execution_id')
    date = execution_group_match.group('date')
    kind = execution_group_match.group('kind')

    s3_prefix = f'{subscription}/{execution_id}/{date}/{kind}'

    full = \
        get_execution_attr_full(s3_client, s3_prefix)
    metadata_attrs = \
        get_metadata_attrs(s3_client, s3_prefix)
    vulnerabilities: dict = \
        get_vulnerability_attrs(
            s3_client, s3_prefix, metadata_attrs['git_repo'])

    return Execution(
        subscription=subscription,
        execution_id=execution_id,
        date=datetime.datetime.strptime(date, LOGS_DATE_FMT),
        kind=kind,
        log=full,
        vulnerabilities=vulnerabilities,
        vulnerabilities_exploits=vulnerabilities[
            'exploits'],
        vulnerabilities_mocked_exploits=vulnerabilities[
            'mocked_exploits'],
        vulnerabilities_accepted_exploits=vulnerabilities[
            'accepted_exploits'],
        vulnerability_count_exploits=vulnerabilities[
            'vulnerability_count_exploits'],
        vulnerability_count_mocked_exploits=vulnerabilities[
            'vulnerability_count_mocked_exploits'],
        vulnerability_count_accepted_exploits=vulnerabilities[
            'vulnerability_count_accepted_exploits'],
        **metadata_attrs,
    )


def yield_execution_groups(s3_client):
    """Yield patterns like <subscription>/<execution_id>/<date>/<kind>."""
    # use Prefix='subscription' to retrieve only from 1 subscription
    s3_client_paginator = s3_client.get_paginator('list_objects_v2')
    s3_client_paginator_iterator = s3_client_paginator.paginate(
        Bucket=BUCKET,
        Delimiter='string',
        EncodingType='url',
        PaginationConfig={
            'PageSize': 1000,
        }
    )

    initial_date_to_sync_from = get_initial_date_to_sync_from()

    seen_groups = set()
    for response in s3_client_paginator_iterator:
        for content in response['Contents']:
            if '__project__' in content['Key'] \
                    or content['LastModified'] < initial_date_to_sync_from:
                continue

            execution_group_match = REGEX_LOGS_NAME.match(content['Key'])

            if not execution_group_match:
                continue

            primary_key = (
                execution_group_match.group('subscription'),
                execution_group_match.group('execution_id'),
            )

            if primary_key not in seen_groups:
                seen_groups.add(primary_key)
                yield execution_group_match


def batch_iterable(batch_size, iterable):
    """Return batches to be processes from the given iterable."""
    batch = []
    count = 0
    for element in iterable:
        count += 1
        batch.append(element)
        if count == batch_size:
            yield batch.copy()
            batch.clear()
            count = 0
    yield batch


def load_executions_to_database() -> bool:
    """Process the s3 logs and load richfull data to the database."""
    utils.aws_login()
    s3_client = boto3.client('s3')
    max_put_items = 25
    with multiprocessing.pool.ThreadPool(processes=1) as pool:
        for batch in batch_iterable(
                max_put_items, yield_execution_groups(s3_client)):
            results = pool.starmap(
                get_execution_object, zip(repeat(s3_client), batch))
            logger.info('Writing to the database')
            for result in results:
                logger.info(
                    f'  - {result.subscription} {result.execution_id}')
                try:
                    result.save()
                except (botocore.exceptions.ClientError,
                        pynamodb.exceptions.PynamoDBException):
                    logger.error('  The following exception was raised')
                    logger.error(traceback.format_exc())
                logger.info('  Cooling down 10 seconds')
                time.sleep(10)
        logger.info('Done')

    return True
