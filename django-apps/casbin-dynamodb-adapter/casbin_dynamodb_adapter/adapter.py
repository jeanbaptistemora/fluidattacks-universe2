"""Casbin DynamoDB Adapter."""

# Standard library
import contextlib
import logging
import os
import re
import uuid
from typing import (
    Iterable,
    List,
    Pattern,
)

# Third parties libraries
import boto3
import botocore
from casbin import persist
from boto3_type_annotations import dynamodb


# Adapter configuration vars
CASBIN_ADAPTER_ENDPOINT_URL = \
    os.environ.get('CASBIN_ADAPTER_ENDPOINT_URL')
CASBIN_ADAPTER_TABLE_NAME = \
    os.environ.get('CASBIN_ADAPTER_TABLE_NAME', 'casbin')
CASBIN_ADAPTER_TABLE_READ_CAPACITY_UNITS = int(
    os.environ.get('CASBIN_ADAPTER_TABLE_READ_CAPACITY_UNITS', '1'))
CASBIN_ADAPTER_TABLE_WRITE_CAPACITY_UNITS = int(
    os.environ.get('CASBIN_ADAPTER_TABLE_WRITE_CAPACITY_UNITS', '1'))

# Constants
POLICY_VALUES_REGEX: str = r'^[a-zA-Z0-9@.]+$'
POLICY_VALUES_PATTERN: Pattern = re.compile(POLICY_VALUES_REGEX)


def create_policy_table(
        dynamodb_resource: dynamodb.ServiceResource,
        table_name: str):
    """Create a Casbin policy table."""
    dynamodb_resource.create_table(
        AttributeDefinitions=[{
            'AttributeName': 'id',
            'AttributeType': 'S',
        }],
        KeySchema=[{
            'AttributeName': 'id',
            'KeyType': 'HASH',
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': CASBIN_ADAPTER_TABLE_READ_CAPACITY_UNITS,
            'WriteCapacityUnits': CASBIN_ADAPTER_TABLE_WRITE_CAPACITY_UNITS,
        },
        TableName=table_name,
    )


def does_table_exist(
        dynamodb_resource: dynamodb.ServiceResource,
        table_name: str) -> bool:
    """Check if a DynamoDB table exists."""
    exists: bool = False
    with contextlib.suppress(botocore.exceptions.ClientError):
        table: dynamodb.Table = dynamodb_resource.Table(table_name)
        exists = table.table_status == 'ACTIVE'
    return exists


def put_policy(
        policy_table: dynamodb.Table,
        policy_type: str,
        rule: List[str]):
    """Insert a policy into the database."""
    unique_id: str = str(uuid.uuid4())

    validate_rule(rule)

    policy_table.put_item(Item={
        'id': unique_id,
        'ptype': policy_type,
        'rule': rule,
    })


def delete_policy(
        policy_table: dynamodb.Table,
        policy_type: str,
        rule: List[str]):
    """Delete a policy from the database."""
    for item in yield_items_from_table(policy_table):
        item_id: str = item['id']
        item_policy_type: str = policy_type
        item_rule: List[str] = item['rule']

        if policy_type == item_policy_type \
                and rule == item_rule:
            policy_table.delete_item(Key={
                'id': item_id,
            })


def validate_rule(rule: List[str]):
    for element in rule:
        if not isinstance(element, str):
            raise ValueError(
                f'Rule elements must be str, got {type(element)}: {element}')

        if not POLICY_VALUES_PATTERN.match(element):
            raise ValueError(
                f'Rule elements must comply regex: {POLICY_VALUES_REGEX}, '
                f'got: {element}')


def yield_items_from_table(table: dynamodb.Table) -> Iterable:
    """Yield items from table."""
    response = table.scan()
    yield from response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'])
        yield from response['Items']


class Adapter(persist.Adapter):
    """The interface for Casbin adapters."""

    table_name = CASBIN_ADAPTER_TABLE_NAME

    def __init__(self):
        """Init constructor method."""
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'))

        self.logger = logging.getLogger('casbin_dynamo_adapter')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.dynamodb_resource: dynamodb.ServiceResource = \
            boto3.resource(
                service_name='dynamodb',
                endpoint_url=CASBIN_ADAPTER_ENDPOINT_URL)

        if not does_table_exist(self.dynamodb_resource, self.table_name):
            create_policy_table(self.dynamodb_resource, self.table_name)

        # pylint: disable=no-member
        self.policy_table = self.dynamodb_resource.Table(self.table_name)

    def load_policy(self, model):
        """Load all policy rules from the storage."""
        for item in yield_items_from_table(self.policy_table):
            item.pop('id', None)

            rule = ', '.join(item.values())
            self.logger.info('AdapterRule: %s', rule)

            persist.load_policy_line(rule, model)

    def save_policy(self, model):
        """Save all policy rules to the storage."""
        for sec in ['p', 'g']:
            if sec not in model.model.keys():
                continue
            for policy_type, ast in model.model[sec].items():
                for rule in ast.policy:
                    put_policy(self.policy_table, policy_type, rule)

    def add_policy(self, sec: str, policy_type: str, rule: List[str]):
        """Add a policy rule to the storage."""
        # pylint: disable=arguments-differ
        put_policy(self.policy_table, policy_type, rule)

    def remove_policy(self, sec: str, policy_type: str, rule: List[str]):
        """Remove a policy rule from the storage."""
        # pylint: disable=arguments-differ
        delete_policy(self.policy_table, policy_type, rule)

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """Remove policy rules that match the filter from the storage."""
        return 'Not implemented'
