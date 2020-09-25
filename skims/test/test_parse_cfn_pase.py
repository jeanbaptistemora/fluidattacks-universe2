# Local libraries
from parse_cfn.parse_yaml import (
    loads as loads_yaml, )
from parse_json.improved import (
    blocking_loads as loads_json, )

EXPECTED = {
    'AWSTemplateFormatVersion': '2010-09-09',
    'Description': 'test',
    'Parameters': {
        'pTest': {
            'Description': 'description',
            'Type': 'type'
        }
    },
    'Resources': {
        'rTest': {
            'Type': 'AWS::RDS::OptionGroup',
            'Properties': {
                'EngineName':
                'mysql',
                'OptionGroupDescription': {
                    'Ref': 'AWS::StackName'
                },
                'Tags': [{
                    'Key': 'Name',
                    'Value': {
                        'Fn::Join':
                        ['', [{
                            'Ref': 'AWS::StackName'
                        }, '-option-group']]
                    }
                }],
                'X':
                True,
                'Y':
                None,
                'days':
                12,
                'capacity':
                123.325
            }
        }
    }
}


def test_load_yaml() -> None:
    with open('test/data/parse_cfn/parse_cnf.yaml') as reader:
        assert loads_yaml(reader.read()) == EXPECTED


def test_load_json() -> None:
    with open('test/data/parse_cfn/parse_cnf.yaml.json') as reader:
        assert loads_json(reader.read()) == EXPECTED


def test_line_and_column_yaml() -> None:
    with open('test/data/parse_cfn/parse_cnf.yaml') as reader:
        template = loads_yaml(reader.read())

        assert template['Description'].__line__ == 3
        assert template['Description'].__column__ == 14
        assert template['Description'] == 'test'

        assert template['Parameters']['pTest']['Type'] == 'type'
        assert template['Parameters']['pTest'].__line__ == 7
        assert template['Parameters']['pTest']['Description'].__column__ == 18

        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription'].__line__ == 16
        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription'].__column__ == 31
        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription']['Ref'].__column__ == 31

        assert template['Resources']['rTest']['Properties'][
            'Tags'].__line__ == 18
        assert template['Resources']['rTest']['Properties']['Tags'][
            0].__line__ == 18
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Key'].__line__ == 18
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value'].__line__ == 19
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value'].__column__ == 18
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][0].__column__ == 25
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][0]['Ref'].__column__ == 30
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][1].__column__ == 54

        assert template['Resources']['rTest']['Properties']['days'] == 12
        assert template['Resources']['rTest']['Properties'][
            'days'].__line__ == 22
        assert template['Resources']['rTest']['Properties'][
            'days'].__column__ == 13

        assert template['Resources']['rTest']['Properties'][
            'capacity'] == 123.325
        assert template['Resources']['rTest']['Properties'][
            'capacity'].__line__ == 23
        assert template['Resources']['rTest']['Properties'][
            'capacity'].__column__ == 17


def test_line_and_column_json() -> None:
    with open('test/data/parse_cfn/parse_cnf.yaml.json') as reader:
        template = loads_json(reader.read())

        assert template['Description'].__line__ == 3
        assert template['Description'].__column__ == 18
        assert template['Description'] == 'test'

        assert template['Parameters']['pTest']['Type'] == 'type'
        assert template['Parameters']['pTest'].__line__ == 5
        assert template['Parameters']['pTest']['Description'].__column__ == 22

        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription'].__line__ == 15
        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription'].__column__ == 35
        assert template['Resources']['rTest']['Properties'][
            'OptionGroupDescription']['Ref'].__column__ == 18

        assert template['Resources']['rTest']['Properties'][
            'Tags'].__line__ == 18
        assert template['Resources']['rTest']['Properties']['Tags'][
            0].__line__ == 19
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Key'].__line__ == 20
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value'].__line__ == 21
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value'].__column__ == 22
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][0].__column__ == 17
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][0]['Ref'].__column__ == 28
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][0]['Ref'].__line__ == 26
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][1].__column__ == 19
        assert template['Resources']['rTest']['Properties']['Tags'][0][
            'Value']['Fn::Join'][1][1].__line__ == 28

        assert template['Resources']['rTest']['Properties']['days'] == 12
        assert template['Resources']['rTest']['Properties'][
            'days'].__line__ == 36
        assert template['Resources']['rTest']['Properties'][
            'days'].__column__ == 17

        assert template['Resources']['rTest']['Properties'][
            'capacity'] == 123.325
        assert template['Resources']['rTest']['Properties'][
            'capacity'].__line__ == 37
        assert template['Resources']['rTest']['Properties'][
            'capacity'].__column__ == 21
