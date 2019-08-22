from decimal import Decimal

import logging
import pytest
import os
from django.db import connections
from django.conf import settings
from moto import mock_dynamodb2
import boto3
from boto3.dynamodb.conditions import Key

from app.dal import finding, integrates_dal

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(scope='function')
def create_users_table():
    with connections['integrates'].cursor() as cursor:
        query = 'CREATE TABLE IF NOT EXISTS users ( \
id INT NOT NULL AUTO_INCREMENT, username varchar(64) COLLATE utf8_general_ci \
DEFAULT NULL, registered tinyint(1) NOT NULL DEFAULT 0, \
last_name varchar(100) COLLATE utf8_general_ci DEFAULT NULL, \
first_name varchar(100) COLLATE utf8_general_ci DEFAULT NULL, \
email varchar(254) COLLATE utf8_general_ci NOT NULL, company varchar(254), \
role varchar(32) NOT NULL, last_login datetime(6) DEFAULT NULL, \
date_joined datetime(6) DEFAULT NULL, PRIMARY KEY (id, email)) ENGINE=INNODB \
DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;'
        add_user_query = 'INSERT INTO users(username, registered, \
last_name, first_name, email, role, last_login, date_joined) \
VALUES ("testing", 1, "testing", "testing", "unittest", "admin", \
        "1111-1-1 11:11:11", "1111-1-1 11:11:11")'
        cursor.execute(query)
        cursor.execute(add_user_query)


@pytest.fixture(scope='function')
def create_projects_table():
    with connections['integrates'].cursor() as cursor:
        query = 'CREATE TABLE IF NOT EXISTS projects ( \
id INT NOT NULL AUTO_INCREMENT, project varchar(64) COLLATE utf8_general_ci \
NOT NULL, description varchar(254) COLLATE utf8_general_ci NOT NULL, \
PRIMARY KEY (id)) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;'
        cursor.execute(query)


@pytest.fixture(scope='function')
def create_project_access_table():
    with connections['integrates'].cursor() as cursor:
        query = 'CREATE TABLE IF NOT EXISTS project_access ( \
user_id INT NOT NULL, project_id INT NOT NULL, has_access tinyint(1) \
NOT NULL DEFAULT 1, FOREIGN KEY (user_id) REFERENCES users(id), \
FOREIGN KEY (project_id) REFERENCES projects(id) \
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;'
        cursor.execute(query)


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def mock_dal_dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource(service_name='dynamodb', region_name='us-east-1')


@pytest.fixture(scope='function')
def mock_dynamodb_table_fi_findings(mock_dal_dynamodb):
    integrates_dal.DYNAMODB_RESOURCE = mock_dal_dynamodb
    table = integrates_dal.DYNAMODB_RESOURCE.create_table(
        TableName='FI_findings',
        KeySchema=[
            {
                'AttributeName': 'finding_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'finding_id',
                'AttributeType': 'S'
            }
        ]
    )
    table.put_item(
        TableName='FI_findings',
        Item={
            'finding_id': '422286126',
            'actor': 'ANYONE_INTERNET',
            'affected_system': 'Server bWAPP\nAnother Server',
            'analyst': 'oparada@fluidattacks.com',
            'attack_complexity': Decimal(0.77).quantize(Decimal('0.10')),
            'attack_vector': Decimal(0.62).quantize(Decimal('0.10')),
            'attack_vector_desc': 'this is an attack vector',
            'availability_impact': '0',
            'availabilityRequirement': 1,
            'client_project': 'Fluid',
            'confidentialityImpact': 0,
            'confidentialityRequirement': 1,
            'context': 'SEARCHING',
            'cvss_basescore': Decimal(3.5).quantize(Decimal('0.1')),
            'cvss_env': Decimal(2.9).quantize(Decimal('0.1')),
            'cvss_basescore': Decimal(3.5).quantize(Decimal('0.1')),
            'cvss_temporal': Decimal(2.9).quantize(Decimal('0.1')),
            'cvssVersion': '3',
            'cwe': '200',
            'effect_solution': 'Implement password politicies with the best \
                                practicies for strong passwords.',
            'exploitability': Decimal(0.91).quantize(Decimal('0.10')),
            'files': [
                {'M': {
                    'description': {'S': 'aaaaa'},
                    'file_url': {'S': 'unittesting-422286126-53713035-test.png'},
                    'name': {'S': 'evidence_route_2'}
                    }
                 },
                {'M': {
                    'description': {'S': 'Im pretty sure it works'},
                    'file_url': {'S':
                                 'unittesting-422286126-53714414-evidencia.png'
                                 },
                    'name': {'S': 'evidence_route_4'}
                    }
                 },
                {'M': {
                    'file_url': {'S':
                                 'unittesting-422286126-49412246-Untitled 1.csv'
                                 },
                    'name': {'S': 'fileRecords'}
                    }
                 },
                {'M': {
                    'file_url': {'S':
                                 'unittesting-422286126-38307199-exploit.py'
                                 },
                    'name': {'S': 'exploit'}
                    }
                 },
                {'M': {
                    'description': {'S': 'yes, it does.'},
                    'file_url': {'S':
                                 'unittesting-422286126-53714452-l.png'
                                 },
                    'name': {'S': 'evidence_route_5'}
                    }
                 },
                {'M': {
                    'file_url': {'S':
                                 'unittesting-422286126-38307272-testFile.gif'
                                 },
                    'name': {'S': 'animation'}
                    }
                 },
                {'M': {
                    'file_url': {'S':
                                 'unittesting-422286126-38307222-a.png'
                                 },
                    'name': {'S': 'exploitation'}
                    }
                 },
                {'M': {
                    'description': {'S': 'this is a test description'},
                    'file_url': {'S':
                                 'unittesting-422286126-32202896-logo.png'
                                 },
                    'name': {'S': 'evidence_route_1'}
                    }
                 },
                {'M': {
                    'description': {'S': 'update test'},
                    'file_url': {'S': 'unittesting-422286126-53713045-a.png'},
                    'name': {'S': 'evidence_route_3'}
                    }
                 }
                ],
            'finding': 'FIN.S.0051. Weak passwords reversed',
            'finding_type': 'SECURITY',
            'id': '422286126',
            'integrityImpact': Decimal(0.22).quantize(Decimal('0.10')),
            'integrityRequirement': 1,
            'interested': 'jrestrepo@fluidattacks.com',
            'last_vulnerability': '2018-11-20',
            'leader': 'jrestrepo@fluidattacks.com',
            'modifiedAttackComplexity': Decimal(0.77).quantize(Decimal('0.10')),
            'modifiedAttackVector': Decimal(0.62).quantize(Decimal('0.10')),
            'modifiedAvailabilityImpact': 0,
            'modifiedConfidentialityImpact': 0,
            'modifiedIntegrityImpact': Decimal(0.22).quantize(Decimal('0.10')),
            'modifiedPrivilegesRequired': Decimal(0.62).quantize(Decimal('0.10')),
            'modifiedSeverityScope': 0,
            'modifiedUserInteraction': Decimal(0.85).quantize(Decimal('0.10')),
            'privilegesRequired': Decimal(0.62).quantize(Decimal('0.10')),
            'project_name': 'unittesting',
            'records': 'Clave plana\nLogin',
            'records_number': '12',
            'remediationLevel': Decimal(0.97).quantize(Decimal('0.10')),
            'reportConfidence': Decimal(0.92).quantize(Decimal('0.10')),
            'report_date': '2018-07-09 07:23:14',
            'report_level': 'GENERAL',
            'requirements': 'REQ.0132. Passwords (phrase type) \
                             must be at least 3 words long.',
            'scenario': 'UNAUTHORIZED_USER_EXTRANET',
            'severity': 0,
            'severityScope': 0,
            'subscription': 'CONTINUOUS',
            'test_type': 'SOURCE_CODE',
            'threat': 'A attack can get passwords  of users and He \
                       can impersonate them or used the credentials for \
                       practices maliciosus.',
            'treatment': 'IN PROGRESS',
            'treatment_justification': 'Test 123',
            'treatment_manager': 'continuoushacking@gmail.com',
            'userInteraction': Decimal(0.85).quantize(Decimal('0.10')),
            'verification_date': '2019-08-21 13:37:15',
            'verification_request_date': 'true',
            'vulnerability': 'It\'s possible reverse the users credentials due\
                    that password policies no force to the users to used  good\
                    practices for strong credentials in the system. \
                    Test\
                    Line\
                    break'
        }
    )
    finding.TABLE = integrates_dal.DYNAMODB_RESOURCE.Table('FI_findings')
