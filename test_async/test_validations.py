import os
import pytest

from django.test import TestCase

from backend.utils.validations import (
    validate_email_address, validate_fields, validate_field_length,
    validate_file_name, validate_project_name, validate_alphanumeric_field,
    validate_phone_field
)
from backend.exceptions import InvalidChar, InvalidField, InvalidFieldLength


class ValidationsTests(TestCase):

    def test_validate_fields(self):
        assert not bool(validate_fields(['testfield', 'testfield2']))
        with pytest.raises(InvalidChar):
            assert validate_fields(['=testfield', 'testfield2'])
            assert validate_fields(['testfield', 'testfiel\'d'])
            assert validate_fields(['testfield', '<testfield2'])
    
    def test_validate_field_length(self):
        assert not bool(validate_field_length('testlength', limit=12))
        assert not bool(validate_field_length('testlength', limit=2, is_greater_than_limit= False))
        with pytest.raises(InvalidFieldLength):
            assert validate_field_length('testlength', limit=9)
            assert validate_field_length('testlength', limit=11, is_greater_than_limit=False)

    def test_validate_email_address(self):
        assert validate_email_address('test@unittesting.com')
        with pytest.raises(InvalidField):
            assert validate_email_address('testunittesting.com')
            assert validate_email_address('test+1@unittesting.com')

    def test_validate_project_name(self):
        assert not bool(validate_project_name('test'))
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

    def test_validate_file_name(self):
        name = 'test123.py'
        invalid_name = 'test.test.py'
        assert validate_file_name(name)
        assert not validate_file_name(invalid_name)
