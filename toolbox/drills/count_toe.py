# Standard library
import os
import csv
import glob
import logging
from datetime import datetime

# Third party libraries
import ruamel.yaml as yaml
from boto3 import resource
from botocore.exceptions import ClientError


EXCLUDES: tuple = (
    '/bower_components/',
    '/node_modules/',
)
EXCLUDES_BY_SUBS: dict = {
    config['name']:
    config.get('coverage', {}).get('lines', {}).get('exclude', [])
    for config_path in glob.glob('groups/*/config/config.yml')
    for config in (yaml.safe_load(open(config_path)),)
}


def get_dynamodb_resource():
    """Get resource from DynamoDB Database. """
    try:
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_region = os.environ['AWS_DEFAULT_REGION']
    except KeyError as err:
        print("Environment variable " + err.args[0] + " doesn't exist")
        raise

    dynamodb_resource = resource('dynamodb',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 region_name=aws_region)
    return dynamodb_resource


def check_lines(subs, file_csv):
    """Insert lineas.csv"""
    with open(file_csv) as f_csv:
        reader = csv.reader(f_csv)
        next(reader, None)
        (lines, tested_lines, skipped) = (0, 0, 0)
        for row in reader:
            if not row:
                continue
            filename: str = row[0]
            if any(e in filename for e in EXCLUDES) \
                    or any(e in filename for e in EXCLUDES_BY_SUBS[subs]):
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
        print('skipped', file_csv, skipped)
    return (lines, tested_lines)


def check_fields(file_csv):
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


def insert_data(project, lines, tested_lines, fields, tested_fields):
    """Insert data into table"""
    dynamodb_resource = get_dynamodb_resource()
    table_name = 'FI_toe'
    table = dynamodb_resource.Table(table_name)
    try:
        response = table.put_item(Item={
            'project': project,
            'lines': lines,
            'lines_tested': tested_lines,
            'fields': fields,
            'fields_tested': tested_fields,
            'last_update': str(datetime.now().date()),
        })
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        return False


def get_projects(path):
    """Get list of projects"""
    projects = []
    for item in os.listdir(path):
        config_file = os.path.join(path, item, 'config/config.yml')
        project_path = os.path.join(path, item)
        if os.path.exists(config_file):
            projects.append(project_path)
        elif os.path.isdir(project_path):
            projects += (get_projects(project_path))
    projects.sort()
    return projects


def main():
    """main function"""
    logger = logging.getLogger('ERROR')
    logger = logging.getLogger('INFO')
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    path = 'groups'
    projects = get_projects(path)
    for project in projects:
        subs: str = project.replace('groups/', '')
        fields = 0
        tested_fields = 0
        lines = 0
        tested_lines = 0
        inputs_file = os.path.join(project, 'toe/inputs.csv')
        lines_file = os.path.join(project, 'toe/lines.csv')
        project_name = os.path.basename(project).lower()
        if os.path.exists(inputs_file):
            fields, tested_fields = check_fields(inputs_file)
        else:
            pass
        if os.path.exists(lines_file):
            lines, tested_lines = check_lines(subs, lines_file)
        else:
            pass

        response = insert_data(project_name, lines, tested_lines, fields,
                               tested_fields)

        if response:
            logger.info("Insertado exitoso: proyecto: %s, lines: %d, "
                        "tested lines: %d, fields: %d, tested fields: %d",
                        project_name, lines, tested_lines, fields,
                        tested_fields)
        else:
            logger.error("Error insertando, proyecto: %s", project_name)
