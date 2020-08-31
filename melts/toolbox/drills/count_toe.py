# Standard library
import os
import csv
import glob
from datetime import datetime

# Third party libraries
import ruamel.yaml as yaml
import boto3
from botocore.exceptions import ClientError

# Local libraries
from toolbox import (
    logger,
    utils,
)

# Constants
INCLUDES_BY_SUBS: dict = {
    config['name']:
    tuple(rule['regex'] for rule in config['coverage']['lines']['include'])
    for config_path in glob.glob('groups/*/config/config.yml')
    for config in (yaml.safe_load(open(config_path)),)
}
EXCLUDES_BY_SUBS: dict = {
    config['name']:
    tuple(rule['regex'] for rule in config['coverage']['lines']['exclude'])
    for config_path in glob.glob('groups/*/config/config.yml')
    for config in (yaml.safe_load(open(config_path)),)
}


def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_DEFAULT_REGION'],
    )


def count_lines(subs, file_csv):
    """Insert lines.csv"""
    with open(file_csv) as f_csv:
        reader = csv.reader(f_csv)
        next(reader, None)
        (lines, tested_lines, skipped) = (0, 0, 0)
        for row in reader:
            if not row:
                continue
            filename: str = row[0]
            if not utils.file.is_covered(
                    path=filename,
                    include_regexps=INCLUDES_BY_SUBS[subs],
                    exclude_regexps=EXCLUDES_BY_SUBS[subs]):
                skipped += int(row[1]) if row[1] else 0
                continue

            if row[1] != '':
                lines += int(row[1])
            else:
                pass
            if len(row) > 2:
                if row[2] != '':
                    tested_lines += int(row[2])
                else:
                    pass
        logger.info('skipped', file_csv, skipped)
    return (lines, tested_lines)


def count_inputs(file_csv):
    """Insert campos.csv"""
    with open(file_csv) as f_csv:
        reader = csv.reader(f_csv)
        next(reader, None)
        (fields, tested_fields) = (0, 0)
        for row in reader:
            if row[1] != '':
                fields += 1
            else:
                pass
            if row[2] == 'Yes':
                tested_fields += 1
            else:
                pass
    return (fields, tested_fields)


def insert_data(group, lines, tested_lines, fields, tested_fields):
    """Insert data into table"""
    success: bool = True
    table = get_dynamodb_resource().Table('FI_toe')
    try:
        response = table.put_item(Item={
            'project': group,
            'lines': lines,
            'lines_tested': tested_lines,
            'fields': fields,
            'fields_tested': tested_fields,
            'last_update': str(datetime.now().date()),
        })
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as exc:
        logger.error(f'Could not insert data for {group}: {exc}')
        success = False
    else:
        logger.info(
            f'{group}, {lines} lines, {tested_lines} tested lines, '
            f'{fields} inputs, {tested_fields} tested inputs'
        )

    return success


def main(target_group: str):
    """main function"""
    success: bool = True

    groups = os.listdir('groups') if target_group == 'all' else [target_group]

    for group in sorted(groups):
        fields, tested_fields, lines, tested_lines = 0, 0, 0, 0

        inputs_file = os.path.join('groups', group, 'toe/inputs.csv')
        lines_file = os.path.join('groups', group, 'toe/lines.csv')

        if os.path.exists(inputs_file):
            fields, tested_fields = count_inputs(inputs_file)

        if os.path.exists(lines_file):
            lines, tested_lines = count_lines(group, lines_file)

        success = success \
            and insert_data(group, lines, tested_lines, fields, tested_fields)

    return success
