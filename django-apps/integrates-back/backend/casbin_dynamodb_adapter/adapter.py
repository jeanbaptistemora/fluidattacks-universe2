"""Casbin DynamoDB Adapter."""

import logging

from botocore.exceptions import ClientError
from casbin import persist

from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE


class Adapter(persist.Adapter):
    """The interface for Casbin adapters."""

    table_name = 'fi_casbin_rule'

    def __init__(self):
        """Init constructor method."""
        self.logger = logging.getLogger('casbin_dynamo_adapter')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if not self.__table_exists():
            self.__create_table()

    def __table_exists(self):
        """Check if database exists."""
        try:
            table = DYNAMODB_RESOURCE.Table(self.table_name)
            return table.table_status == 'ACTIVE'
        except ClientError:
            return False

    def __create_table(self):
        """Create casbin rule table."""
        DYNAMODB_RESOURCE.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH',
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            },
            TableName=self.table_name,
        )

    def __get_all_rules(self):
        """Retrieve all rules from table."""
        rules = DYNAMODB_RESOURCE.Table(self.table_name).scan()['Items']
        return rules

    def load_policy(self, model):
        """Load all policy rules from the storage."""
        rules = self.__get_all_rules()
        for _rule in rules:
            _rule.pop('id', None)
            rule = ', '.join(_rule.values())
            self.logger.info('Adapter_Rule: %s', str(rule))
            persist.load_policy_line(str(rule), model)

    def _save_policy_line(self, ptype, rule):
        line = {'ptype': ptype}
        for counter, value in enumerate(rule):
            setattr(line, f'v{counter}', value)
        table = DYNAMODB_RESOURCE.Table(self.table_name)
        table.put_item(Item=line)

    def save_policy(self, model):
        """Save all policy rules to the storage."""
        for sec in ['p', 'g']:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        """Add a policy rule to the storage."""
        self._save_policy_line(ptype, rule)

    def remove_policy(self, sec, ptype, rule):
        """Remove a policy rule from the storage."""
        return 'Not implemented'

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """Remove policy rules that match the filter from the storage."""
        return 'Not implemented'
