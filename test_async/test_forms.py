import pytest
from datetime import datetime

from backend.utils.forms import (
    dict_concatenation, is_exploitable
)

from django.test import TestCase
from numpy import arange


class FormsTests(TestCase):

    @pytest.mark.no_changes_db
    def test_dict_concatenation(self):
        dict_1 = {'element': 'hi', 'element2': 'how are'}
        dict_2 = {'element3': 'you'}
        test_data = dict_concatenation(dict_1, dict_2)
        expected_output = {
            'element': 'hi',
            'element2': 'how are',
            'element3': 'you'}
        assert test_data == expected_output

    @pytest.mark.no_changes_db
    def test_is_exploitable(self):
        version = '3.1'
        for exploitability in arange(0.0, 0.96, 0.2):
            assert is_exploitable(exploitability, version) == 'No'
        for exploitability in arange(0.97, 2, 0.3):
            assert is_exploitable(exploitability, version) == 'Si'
        version = '2'
        exploitble_exploitabilities = [1.0, 0.95]
        for exploitability in exploitble_exploitabilities:
            assert is_exploitable(exploitability, version) == 'Si'
        non_exploitable_exploitability = 0.5
        assert is_exploitable(non_exploitable_exploitability, version) == 'No'
