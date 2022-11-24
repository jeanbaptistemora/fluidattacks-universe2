from parse_cfn.loader import (
    load_as_json,
    load_as_yaml,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_load_as_json() -> None:
    expected = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "test",
        "Parameters": {
            "__column__": 5,
            "__line__": 5,
            "pTest": {
                "Description": "description",
                "Type": "type",
                "__column__": 7,
                "__line__": 6,
            },
        },
        "Resources": {
            "__column__": 5,
            "__line__": 11,
            "rTest": {
                "Properties": {
                    "EngineName": "mysql",
                    "OptionGroupDescription": {
                        "Ref": "AWS::StackName",
                        "__column__": 11,
                        "__line__": 16,
                    },
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Ref": "AWS::StackName",
                                            "__column__": 21,
                                            "__line__": 26,
                                        },
                                        "-option-group",
                                    ],
                                ],
                                "__column__": 15,
                                "__line__": 22,
                            },
                            "__column__": 13,
                            "__line__": 20,
                        }
                    ],
                    "X": True,
                    "Y": None,
                    "__column__": 9,
                    "__line__": 14,
                },
                "Type": "AWS::RDS::OptionGroup",
                "__column__": 7,
                "__line__": 12,
            },
        },
        "__column__": 3,
        "__line__": 2,
    }

    with open(
        "skims/test/data/parse_cfn/1.yaml.json", encoding="utf-8"
    ) as file:
        assert load_as_json(file.read()) == expected


@pytest.mark.skims_test_group("unittesting")
def test_load_as_yaml() -> None:
    expected = {
        "__column__": 0,
        "__line__": 2,
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "test",
        "Parameters": {
            "__column__": 2,
            "__line__": 6,
            "pTest": {
                "__column__": 4,
                "__line__": 7,
                "Description": "description",
                "Type": "type",
            },
        },
        "Resources": {
            "__column__": 2,
            "__line__": 12,
            "rTest": {
                "__column__": 4,
                "__line__": 13,
                "Properties": {
                    "__column__": 6,
                    "__line__": 15,
                    "EngineName": "mysql",
                    "OptionGroupDescription": {
                        "__column__": 30,
                        "__line__": 16,
                        "Ref": "AWS::StackName",
                    },
                    "Tags": [
                        {
                            "__column__": 10,
                            "__line__": 18,
                            "Key": "Name",
                            "Value": {
                                "__column__": 17,
                                "__line__": 19,
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "__column__": 29,
                                            "__line__": 19,
                                            "Ref": "AWS::StackName",
                                        },
                                        "-option-group",
                                    ],
                                ],
                            },
                        },
                    ],
                    "X": True,
                    "Y": None,
                },
                "Type": "AWS::RDS::OptionGroup",
            },
        },
    }

    with open("skims/test/data/parse_cfn/1.yaml", encoding="utf-8") as file:
        assert load_as_yaml(file.read()) == expected
