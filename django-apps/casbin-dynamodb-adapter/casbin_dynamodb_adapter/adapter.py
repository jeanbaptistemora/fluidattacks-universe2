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
    Set,
)

# Third parties libraries
import boto3
import botocore
from casbin import persist
from boto3_type_annotations import dynamodb


# Adapter configuration vars
CASBIN_ADAPTER_ENDPOINT_URL = \
    os.environ.get('CASBIN_ADAPTER_ENDPOINT_URL') or None
CASBIN_ADAPTER_TABLE_NAME = \
    os.environ.get('CASBIN_ADAPTER_TABLE_NAME', 'casbin')
CASBIN_ADAPTER_TABLE_READ_CAPACITY_UNITS = int(
    os.environ.get('CASBIN_ADAPTER_TABLE_READ_CAPACITY_UNITS', '1'))
CASBIN_ADAPTER_TABLE_WRITE_CAPACITY_UNITS = int(
    os.environ.get('CASBIN_ADAPTER_TABLE_WRITE_CAPACITY_UNITS', '1'))

# Constants
POLICY_VALUES_REGEX: str = r'^[a-zA-Z0-9@._+-]+$'
POLICY_VALUES_PATTERN: Pattern = re.compile(POLICY_VALUES_REGEX)

# Types
Attribute = str
Rule = List[Attribute]


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


def get_rules(
        policy_table: dynamodb.Table,
        policy_type: str,
        partial_rule: Rule) -> List[Rule]:
    """Return rules matching partially from the database."""
    results: List[Rule] = []
    partial_rule_len: int = len(partial_rule)
    for item in yield_items_from_table(policy_table):
        item_policy_type: str = item['policy_type']
        item_rule: Rule = item['rule']

        if policy_type == item_policy_type \
                and partial_rule == item_rule[0:partial_rule_len]:
            results.append(item_rule)

    return results


def put_policy(
        policy_table: dynamodb.Table,
        policy_type: str,
        rule: Rule):
    """Insert a policy into the database."""
    unique_id: str = str(uuid.uuid4())

    validate_rule(rule)

    policy_table.put_item(Item={
        'id': unique_id,
        'policy_type': policy_type,
        'rule': rule,
    })


def delete_policy(
        policy_table: dynamodb.Table,
        policy_type: str,
        partial_rule: Rule):
    """Delete a policy from the database."""
    partial_rule_len: int = len(partial_rule)
    for item in yield_items_from_table(policy_table):
        item_id: str = item['id']
        item_policy_type: str = item['policy_type']
        item_rule: Rule = item['rule']

        if policy_type == item_policy_type \
                and partial_rule == item_rule[0:partial_rule_len]:
            policy_table.delete_item(Key={
                'id': item_id,
            })


def validate_rule(rule: Rule):
    for attribute in rule:
        if not isinstance(attribute, Attribute):
            raise TypeError(
                f'Rule attributes must be of type: {Attribute}, '
                f'got {type(attribute)}: {attribute}')

        if not POLICY_VALUES_PATTERN.match(attribute):
            raise ValueError(
                f'Rule attributes must comply regex: {POLICY_VALUES_REGEX}, '
                f'got: {attribute}')


def deduplicate_policies(policy_table: dynamodb.Table):
    """Delete unneeded items from the database."""
    seen_items: Set[tuple] = set()

    for item in yield_items_from_table(policy_table):
        item_id: str = item['id']
        item_policy_type: str = item['policy_type']
        item_rule: Rule = item['rule']

        item_hash: tuple = (item_policy_type, tuple(item_rule))

        if item_hash in seen_items:
            policy_table.delete_item(Key={
                'id': item_id,
            })
        else:
            seen_items.add(item_hash)


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

            rule: Rule = []
            rule.append(item['policy_type'])
            rule.extend(item['rule'])

            rule_csv = ', '.join(rule)

            self.logger.info('AdapterRule: %s', rule_csv)

            persist.load_policy_line(rule_csv, model)

    def save_policy(self, model):
        """Save all policy rules to the storage."""
        for section in ['p', 'g']:
            if section not in model.model.keys():
                continue
            for policy_type, assertion in model.model[section].items():
                for rule in assertion.policy:
                    put_policy(self.policy_table, policy_type, rule)

    def add_policy(self, sec: str, policy_type: str, rule: Rule):
        """Add a policy rule to the storage."""
        # pylint: disable=arguments-differ
        put_policy(self.policy_table, policy_type, rule)

    def remove_policy(self, sec: str, policy_type: str, partial_rule: Rule):
        """Remove a policy rule from the storage."""
        # pylint: disable=arguments-differ
        delete_policy(self.policy_table, policy_type, partial_rule)

    def get_rules(self, policy_type: str, partial_rule: Rule) -> List[Rule]:
        """Return rules matching criteria from the database."""
        return get_rules(self.policy_table, policy_type, partial_rule)

    def deduplicate_policies(self):
        """Delete unneeded items from the database."""
        deduplicate_policies(self.policy_table)

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """Remove policy rules that match the filter from the storage."""
        return 'Not implemented'
