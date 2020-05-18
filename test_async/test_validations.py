import os
import pytest

from django.test import TestCase

from backend.utils.validations import (
    validate_email_address, validate_fields, validate_project_name,
    validate_alphanumeric_field, validate_phone_field
)
from backend.exceptions import InvalidChar, InvalidField


class ValidationsTests(TestCase):

    def test_validate_fields(self):
        assert validate_fields(['testfield', 'testfield2']) == None
        with pytest.raises(InvalidChar):
            assert validate_fields(['=testfield', 'testfield2'])
            assert validate_fields(['testfield', 'testfiel\'d'])
            assert validate_fields(['testfield', '<testfield2'])

    def test_validate_email_address(self):
        assert validate_email_address('test@unittesting.com')
        with pytest.raises(InvalidField):
            assert validate_email_address('testunittesting.com')

    def test_validate_project_name(self):
        assert validate_project_name('test') == None
        with pytest.raises(InvalidField):
            assert validate_project_name('=test2@')

    def test_validate_alphanumeric_field(self):
        assert validate_alphanumeric_field('one test')
        with pytest.raises(InvalidField):
            assert validate_alphanumeric_field('=test2@')

    def test_validate_phone_field(self):
        assert validate_phone_field('+57123')
        with pytest.raises(InvalidField):
            assert validate_phone_field('+')
