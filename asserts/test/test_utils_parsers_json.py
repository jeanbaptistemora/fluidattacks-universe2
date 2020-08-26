# 3rd party imports
from fluidasserts.utils.parsers import json
import pytest
pytestmark = pytest.mark.asserts_module('utils')


def test_parser():
    """Test JSON parser"""
    test_json = '''
        {
            "empty_object" : {},
            "object"       : {
                                "user_name": "jane doe",
                                "age": 20
                             },
            "empty_array"  : [],
            "booleans"     : { "YES" : true, "NO" : false },
            "numbers"      : [ 0, 1, -2, 3.3, 4.4e5, 6.6e-7 ],
            "strings"      : [ "This", [ "And" , "That", "And a \\"b" ] ],
            "nothing"      : null
        }
    '''
    content = json.parse(test_json)
    test_cases = [
        {'case': content['empty_object.line'],
         'expected': 3},
        {'case': content['empty_object'],
         'expected': {}},
        {'case': content['object']['age'],
         'expected': 20},
        {'case': content['object']['age.line'],
         'expected': 6},
        {'case': content['object']['user_name'],
         'expected': 'jane doe'},
        {'case': content['empty_array.line'],
         'expected': 8},
        {'case': content['empty_array'],
         'expected': []},
        {'case': content['booleans.line'],
         'expected': 9},
        {'case': content['booleans']['YES'],
         'expected': True},
        {'case': content['booleans']['YES.line'],
         'expected': 9},
        {'case': content['booleans']['NO'],
         'expected': False},
        {'case': content['booleans']['NO.line'],
         'expected': 9},
        {'case': content['numbers']['2'],
         'expected': -2.0},
        {'case': content['numbers']['4.line'],
         'expected': 10},
        {'case': content['strings'][0],
         'expected': "This"},
        {'case': content['strings.line'],
         'expected': 11},
        {'case': content['strings'][1]['1'],
         'expected': "That"},
        {'case': content['strings']['1.line'],
         'expected': 11},
        {'case': content['strings'][1]['2.line'],
         'expected': 11},
        {'case': content['nothing'],
         'expected': None},
    ]

    for case in test_cases:
        assert case['case'] == case['expected']
