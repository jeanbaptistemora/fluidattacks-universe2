# Standard library
from datetime import datetime

# Local libraries
from parse_cfn import (
    loads,
)


def test_loads() -> None:
    with open('test/data/parse_cfn/1.yaml') as file:
        data = loads(file.read())

    assert data == {
        '__column__': 0,
        '__line__': 1,
        'AWSTemplateFormatVersion': datetime(2010, 9, 9).date(),
        'Description': 'test',
        'Parameters': {
            '__column__': 2,
            '__line__': 5,
            'pTest': {
                '__column__': 4,
                '__line__': 6,
                'Description': 'description',
                'Type': 'type',
            },
        },
        'Resources': {
            '__column__': 2,
            '__line__': 11,
            'rTest': {
                '__column__': 4,
                '__line__': 12,
                'Properties': {
                    '__column__': 6,
                    '__line__': 14,
                    'EngineName': 'mysql',
                    'OptionGroupDescription': {
                        '__column__': 30,
                        '__line__': 15,
                        'Ref': 'AWS::StackName',
                    },
                    'Tags': [
                        {
                            '__column__': 10,
                            '__line__': 17,
                            'Key': 'Name',
                            'Value': {
                                '__column__': 17,
                                '__line__': 18,
                                'Fn::Join': [
                                    '',
                                    [
                                        {
                                            '__column__': 29,
                                            '__line__': 18,
                                            'Ref': 'AWS::StackName',
                                        },
                                        '-option-group',
                                    ],
                                ],
                            },
                        },
                    ],
                },
                'Type': 'AWS::RDS::OptionGroup',
            },
        },
    }
